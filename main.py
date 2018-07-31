# coding=utf-8
from machinekit import hal
from machinekit import rtapi as rt
from machinekit import config as c


MAIN_THREAD = 'main-thread'


def init_hardware():
    # we need a thread to execute the component functions
    rt.newthread(MAIN_THREAD, 1e6, fp=True)

    rt.loadrt('hal_bb_gpio', output_pins='926,807', input_pins='')
    rt.loadrt(c.find('PRUCONF', 'DRIVER'), 'prucode=' + c.find('PRUCONF', 'PRUBIN'),
              pru=0, num_pwmgens=3, num_stepgens=3, halname='hpg')


def configure_stepgen():
    # stepgen config
    hal.Pin('hpg.stepgen.00.steppin').set(812)
    hal.Pin('hpg.stepgen.00.dirpin').set(811)
    hal.Pin('hpg.stepgen.00.control-type').set(1)  # velocity mode
    hal.Pin('hpg.stepgen.00.position-scale').set(c.find('STEPPER', 'SCALE'))
    hal.Pin('hpg.stepgen.00.dirsetup').set(c.find('STEPPER', 'DIRSETUP'))
    hal.Pin('hpg.stepgen.00.dirhold').set(c.find('STEPPER', 'DIRHOLD'))
    hal.Pin('hpg.stepgen.00.steplen').set(c.find('STEPPER', 'STEPLEN'))
    hal.Pin('hpg.stepgen.00.stepspace').set(c.find('STEPPER', 'STEPSPACE'))
    hal.Pin('hpg.stepgen.00.velocity-cmd').link(hal.Signal('motor-vel', hal.HAL_FLOAT))
    hal.Pin('hpg.stepgen.00.enable').link(hal.Signal('motor-enable', hal.HAL_BIT))

    # machine power
    hal.Pin('bb_gpio.p9.out-26').link(hal.Signal('motor-enable', hal.HAL_BIT))
    hal.Pin('bb_gpio.p8.out-07').link(hal.Signal('motor-enable', hal.HAL_BIT))
    hal.Pin('bb_gpio.p8.out-07.invert').set(True)


def create_rcomp():
    rcomp = hal.RemoteComponent('control', timer=100)
    rcomp.newpin('vel-cmd', hal.HAL_FLOAT, hal.HAL_OUT)
    rcomp.newpin('enable', hal.HAL_BIT, hal.HAL_OUT)
    rcomp.ready()

    rcomp.pin('vel-cmd').link(hal.Signal('motor-vel'))
    rcomp.pin('enable').link(hal.Signal('motor-enable'))


def setup_functions():
    hal.addf('bb_gpio.read', MAIN_THREAD)

    # foo

    hal.addf('hpg.update', MAIN_THREAD)
    hal.addf('bb_gpio.write', MAIN_THREAD)


def main():
    c.load_ini('hardware.ini')

    init_hardware()
    configure_stepgen()
    create_rcomp()
    setup_functions()

    # ready to start the threads
    hal.start_threads()

    # start haltalk server after everything is initialized
    # else binding the remote components on the UI might fail
    hal.loadusr('haltalk', wait=True)


main()
