from jproperties import Properties


class CommonUtil:

    # This method load configuration and returns config data
    @staticmethod
    def read_properties():

        config_filename = 'src/Config/app-config.properties'
        configs = Properties()
        with open(config_filename, 'rb') as read_config_file:
            configs.load(read_config_file)

        return configs




