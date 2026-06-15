import attr
from copy import deepcopy
import numpy as np
from scipy.interpolate import interp1d
from bilby.core.utils import create_time_series
from bilby.core.likelihood import Likelihood

@attr.s(slots=True, weakref_slot=False)
class CalculatedSNRs:
    d_inner_h = attr.ib(default=0j, converter=complex)
    optimal_snr_squared = attr.ib(default=0, converter=float)
    complex_matched_filter_snr = attr.ib(default=0j, converter=complex)

    def __add__(self, other_snr):
        new = deepcopy(self)
        new += other_snr
        return new

    def __iadd__(self, other_snr):
        for key in self.__slots__:
            this = getattr(self, key)
            other = getattr(other_snr, key)
            if this is not None and other is not None:
                setattr(self, key, this + other)
            elif this is None:
                setattr(self, key, other)
        return self

    @property
    def snrs_as_sample(self) -> dict:
        """Get the SNRs of this object as a sample dictionary

        Returns
        =======
        dict
            The dictionary of SNRs labelled accordingly
        """
        return {
            "matched_filter_snr" : self.complex_matched_filter_snr,
            "optimal_snr" : self.optimal_snr_squared.real ** 0.5
        }

class SimpleExtrinsicGWTransient(Likelihood):

    def __init__(self, interferometers, waveform_generator, priors, reference_parameters):
        """

        A likelihood object, able to compute the likelihood of the data given
        some model parameters

        The simplest frequency-domain gravitational wave transient likelihood. Does
        not include distance/phase marginalization.


        Parameters
        ==========
        interferometers: list
            A list of `bilby.gw.detector.Interferometer` instances - contains the
            detector data and power spectral densities
        waveform_generator: bilby.gw.waveform_generator.WaveformGenerator
            An object which computes the frequency-domain strain of the signal,
            given some set of parameters

        """
        super(SimpleExtrinsicGWTransient, self).__init__(dict())
        self.interferometers = interferometers
        self.waveform_generator = waveform_generator
        self.priors = priors
        self.reference_parameters = reference_parameters
        self.waveform_polarizations = \
            self.waveform_generator.frequency_domain_strain(reference_parameters)

        self.start_time = self.interferometers[0].strain_data.start_time
        self.duration = self.waveform_generator.duration

        self.precompute_inner_products()

    def __repr__(self):
        return self.__class__.__name__ + '(interferometers={},\n\twaveform_generator={})' \
            .format(self.interferometers, self.waveform_generator)

    def precompute_inner_products(self):
        hp = self.waveform_polarizations['plus']
        hc = self.waveform_polarizations['cross']

        self.ifos_hp_hp_dict = {}
        self.ifos_hc_hc_dict = {}
        self.ifos_hp_hc_dict = {}

        for ifo in self.interferometers:
            self.ifos_hp_hp_dict[ifo.name] = ifo.optimal_snr_squared(hp).real
            self.ifos_hc_hc_dict[ifo.name] = ifo.optimal_snr_squared(hc).real
            self.ifos_hp_hc_dict[ifo.name] = ifo.template_template_inner_product(hp, hc).real

        self.set_data_inner_arrays(
            self.reference_parameters['geocent_time'], self.priors['geocent_time'], hp, hc
        )

    def set_data_inner_arrays(self, geocent_time, prior, h_plus, h_cross):
        normalisation = 4 / self.duration

        self.ifos_hp_d_dict = {}
        self.ifos_hc_d_dict = {}

        times = create_time_series(
            sampling_frequency=16384, duration=self.duration,
            starting_time=geocent_time - self.start_time)
        times = times % self.duration
        times += self.start_time

        in_prior = (times >= prior.minimum) & (times < prior.maximum)
        in_prior = times > 0
        times = times[in_prior]
        sorted_idx = np.argsort(times)
        times = times[sorted_idx] - self.start_time

        n_time_steps = int(self.duration * 16384)
        psd = np.ones(n_time_steps)
        data = np.zeros(n_time_steps, dtype=complex)
        hp_long, hc_long = np.zeros((2, n_time_steps), dtype=complex)
        hpc_len = len(h_plus)
        phase_shift = np.exp(-1j * 2 * np.pi * (geocent_time - self.start_time) * self.waveform_generator.frequency_array)
        hp_long[:hpc_len] = h_plus * phase_shift
        hc_long[:hpc_len] = h_cross * phase_shift
        for ifo in self.interferometers:
            ifo_length = len(ifo.frequency_domain_strain)
            assert ifo_length == hpc_len
            mask = ifo.frequency_mask

            data[:ifo_length] = ifo.frequency_domain_strain.conjugate()
            psd[:ifo_length][mask] = ifo.power_spectral_density_array[mask]

            _hp_d = np.fft.fft(hp_long * data / psd)[in_prior][sorted_idx]
            _hc_d = np.fft.fft(hc_long * data / psd)[in_prior][sorted_idx]

            self.ifos_hp_d_dict[ifo.name] = interp1d(times, normalisation * _hp_d, assume_sorted=True)
            self.ifos_hc_d_dict[ifo.name] = interp1d(times, normalisation * _hc_d, assume_sorted=True)

    def noise_log_likelihood(self):
        """ Calculates the real part of noise log-likelihood

        Returns
        =======
        float: The real part of the noise log likelihood

        """
        if not hasattr(self, 'd_inner_d'):
            log_l = 0
            for interferometer in self.interferometers:
                log_l -= 2. / self.duration * np.sum(
                    abs(interferometer.frequency_domain_strain) ** 2 /
                    interferometer.power_spectral_density_array)
            self.d_inner_d = log_l.real
        return self.d_inner_d

    def log_likelihood_ratio(self):
        """ Calculates the real part of log-likelihood value

        Returns
        =======
        float: The real part of the log likelihood

        """
        log_l = 0
        for interferometer in self.interferometers:
            log_l += self.single_detector_log_likelihood(interferometer)
        return log_l.real

    def log_likelihood(self):
        return self.log_likelihood_ratio() + self.noise_log_likelihood()

    def single_detector_log_likelihood(self, interferometer):
        """
        Parameters
        ==========
        interferometer: bilby.gw.detector.Interferometer
            The Interferometer object we want to have the log-likelihood for

        Returns
        =======
        float: The real part of the log-likelihood for this interferometer

        """
        snrs = self.calculate_snrs(self.waveform_polarizations, interferometer)
        return snrs.d_inner_h.real - 0.5 * snrs.optimal_snr_squared

    ####################################################
    # Functions below this are here to compatible with some features of CBCResult
    ####################################################

    def compute_per_detector_log_likelihood(self):
        parameters = deepcopy(self.parameters)

        for interferometer in self.interferometers:
            parameters[f'{interferometer.name}_log_likelihood'] = \
                self.single_detector_log_likelihood(interferometer)

        return parameters.copy()

    def calculate_snrs(self, waveform_polarizations, interferometer, return_array=True):
        parameters = deepcopy(self.parameters)
        det = interferometer.name
        Fp = interferometer.antenna_response(
                parameters['ra'], parameters['dec'], 
                parameters['geocent_time'], parameters['psi'], 'plus')
        Fc = interferometer.antenna_response(
                parameters['ra'], parameters['dec'], 
                parameters['geocent_time'], parameters['psi'], 'cross')

        time_shift = interferometer.time_delay_from_geocenter(
            parameters['ra'], parameters['dec'], parameters['geocent_time'])

        dt_geocent = parameters['geocent_time'] - self.start_time
        dt = dt_geocent + time_shift

        h_inner_h = Fp*Fp * self.ifos_hp_hp_dict[det] + \
                    Fc*Fc * self.ifos_hc_hc_dict[det] + \
                    2*Fp*Fc * self.ifos_hp_hc_dict[det]
        h_inner_h *= (self.reference_parameters['luminosity_distance'] / parameters['luminosity_distance']) ** 2

        d_inner_h = Fp * self.ifos_hp_d_dict[det](dt) + \
                    Fc * self.ifos_hc_d_dict[det](dt)
        d_inner_h *= (self.reference_parameters['luminosity_distance'] / parameters['luminosity_distance'])

        return CalculatedSNRs(
            d_inner_h=d_inner_h,
            optimal_snr_squared=h_inner_h,
            complex_matched_filter_snr=d_inner_h / h_inner_h**0.5,
        )