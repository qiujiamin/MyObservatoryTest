# NOTE: Generated By HttpRunner v3.1.4
# FROM: .\har\wed_test.har


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCaseWedTest(HttpRunner):

    config = Config("testcase description").verify(False)

    teststeps = [
        Step(
            RunRequest("/locspc/data/ocf_data/HKO.v2.xml")
            .get("https://pda.weather.gov.hk/locspc/data/ocf_data/HKO.v2.xml")
            .with_headers(
                **{
                    "Host": "pda.weather.gov.hk",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
                    "Referer": "https://pda.weather.gov.hk/locspc/data/ocf_data/graph/arwf/index.html?stationCode=HKO&currentHour=2022110113&device=iOS&theme=light&lang=sc",
                    "Accept-Language": "en-us",
                    "X-Requested-With": "XMLHttpRequest",
                    "Connection": "keep-alive",
                }
            )
            .extract()
            .with_jmespath("body.dailyForecast[0][2].ForecastChanceOfRain", "ForecastChanceOfRain")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal('headers."Content-Type"', "text/xml")
        ),
    ]


if __name__ == "__main__":
    TestCaseWedTest().test_start()
