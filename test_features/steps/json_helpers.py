from hamcrest import assert_that, has_key, has_entry, equal_to


def check_json(json_expected, json_to_search):
    if type(json_expected) is list:

        check_json_list(json_expected, json_to_search)

    elif type(json_expected) is dict:

        for key, value in json_expected.items():

            if type(value) is dict:
                assert_that(json_to_search, has_key(key))
                check_json(value, json_to_search[key])
                check_json(json_to_search[key], value)

            elif type(value) is list:

                for i in range(0, len(value)):
                    check_json(json_expected[key][i], json_to_search[key][i])
                    check_json(json_to_search[key][i], json_expected[key][i])

            else:

                assert_that(json_to_search, has_entry(key, value))
    else:
        assert_that(json_to_search, equal_to(json_expected))


def check_json_list(json_expected, json_to_search):
    for i in range(0, len(json_expected)):
        check_json(json_expected[i], json_to_search[i])
        check_json(json_to_search[i], json_expected[i])
