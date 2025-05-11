# Micropython Time library

[Documentation](https://docs.micropython.org/en/latest/library/time.html)

## Get and convert time

### get current time:

* time.localtime()
* time.gmtime()

### get datetime object of a specific date

**Getting datetime in seconds for the date `2025-05-10 13:25:00`:**
```
>>> time.mktime((2025, 5, 10, 13, 25, 00, None, None))
800226336
```
**And same date but with datetime object:**
```
>>> time.localtime(time.mktime((2025, 5, 10, 13, 25, 00, None, None)))
(2025, 5, 10, 13, 25, 0, 5, 130)
```
### Week days:
  monday: 0
  tuesday: 1
  wednesday: 2
  thursday: 3
  friday: 4
  saturday: 5
  sunday: 6

## Update time with ntp server

**NOTE:** It needs internet access

```
import ntptime

ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()

```

## Time zone adjustment

Currently neither ntptime and machine.RTC supports timezone, so we must do the adjustment manaully:

### Basic adjustment
Manual adjustment with RTC object:


```
from machine import RTC
rtc = RTC()

(year, month, day, weekday, hours, minutes, seconds, subseconds) = rtc.datetime()
rtc.datetime((year, month, day, weekday, hours + 2, minutes, seconds, subseconds))

```

### Dynamic adjustment (TODO)

[Timeapi](https://timeapi.io/) is a web service to get timezone info (and some other time utils/data):

[Timeapi API documentation](https://timeapi.io/swagger/index.html)

We can use this service to get the current time offset based on our timezone:

```
curl -X 'GET' \
  'https://timeapi.io/api/timezone/zone?timeZone=Europe%2FMadrid' \
  -H 'accept: application/json'
```

Response:
```
{
  "timeZone": "Europe/Madrid",
  "currentLocalTime": "2025-05-11T10:28:02.4054762",
  "currentUtcOffset": {
    "seconds": 7200,
    "milliseconds": 7200000,
    "ticks": 72000000000,
    "nanoseconds": 7200000000000
  },
  "standardUtcOffset": {
    "seconds": 3600,
    "milliseconds": 3600000,
    "ticks": 36000000000,
    "nanoseconds": 3600000000000
  },
  "hasDayLightSaving": true,
  "isDayLightSavingActive": true,
  "dstInterval": {
    "dstName": "CEST",
    "dstOffsetToUtc": {
      "seconds": 7200,
      "milliseconds": 7200000,
      "ticks": 72000000000,
      "nanoseconds": 7200000000000
    },
    "dstOffsetToStandardTime": {
      "seconds": 3600,
      "milliseconds": 3600000,
      "ticks": 36000000000,
      "nanoseconds": 3600000000000
    },
    "dstStart": "2025-03-30T01:00:00Z",
    "dstEnd": "2025-10-26T01:00:00Z",
    "dstDuration": {
      "days": 210,
      "nanosecondOfDay": 0,
      "hours": 0,
      "minutes": 0,
      "seconds": 0,
      "milliseconds": 0,
      "subsecondTicks": 0,
      "subsecondNanoseconds": 0,
      "bclCompatibleTicks": 181440000000000,
      "totalDays": 210,
      "totalHours": 5040,
      "totalMinutes": 302400,
      "totalSeconds": 18144000,
      "totalMilliseconds": 18144000000,
      "totalTicks": 181440000000000,
      "totalNanoseconds": 18144000000000000
    }
  }
}
```

`currentUtcOffset.seconds` can be used to calculate the adjustment dynamically.




```
>>> time.localtime()
(2025, 5, 10, 21, 5, 36, 5, 130)
>>> time.time()
800226367
>>>
>>> time.mktime((2025, 5, 10, 21, 5, 36, None, None))
800226336
>>> print(f" time.time is {time.time()} -- time.gmtime is {time.gmtime()}")
 time.time is 800226475 -- time.gmtime is (2025, 5, 10, 21, 7, 55, 5, 130)
>>>
>>> print(f" time.time is {time.time()} -- time.gmtime is {time.gmtime()}")
 time.time is 800226479 -- time.gmtime is (2025, 5, 10, 21, 7, 59, 5, 130)
>>> time.mktime((2025, 5, 10, 21, 7, 59, None, None))
800226479
```


## week days

