"""Datalogger settings"""

# General settings.
main = {

    # these three options are logically exclusive but if you insist: shutoff > deepsleep > lightsleep
    # if all three are false we are in continous mode
    # whether to switch everything off between measurement cycles - requires DS3231 & switch
    'shutoff': False,
    # whether to use deep sleep between measurement cycles
    'deepsleep': False,
    # whether to use ight sleep between measurement cycles
    'lightsleep': False,

    # RTC available
    'RTC': False,
    # get time through NTP
    'NTP': False,

    # Measurement intervals in seconds, for shutoff in minutes.
    'interval': {

        # apply this interval if device goes into shutoff
        'shutoff': 15,  # [min]

        # apply this interval if device goes into deepsleep
        'deepsleep': 10,  # [min]

        # apply this interval if device goes into lightsleep
        'lightsleep': 5,  # [min]

        # apply this delay if the device doesn't sleep at all
        'continous': 1,  # [min]

        # the next options require a valid source of time
        # night & winter mode: during the night or winter the interval is doubled (-> in a winter night it is quadrupled)
        # beginning & end months are included: night from 20 to 5 -> 20.00h to 5.59h, winter from 10 to 2 -> October 1st to February 29th
        # a start value of 0 means there is no night/winter, night_start > night_end, winter_start > winter_end
        'night_start': 20,
        'night_end' : 5,
        'winter_start' : 10,
        'winter_end' : 2,
    },


    # Configure logging.
    'logging': {

        # Enable or disable logging completely.
        'enabled': True,

        # Log configuration settings at system startup.
        'configuration': True,
    },

}