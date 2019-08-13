from ..utils import *
from webbrowser import open as open_url
from csv import DictWriter
from cloudinary.utils import cloudinary_url as cld_url
from cloudinary import api, uploader as _uploader
from click import command, argument, option, Choice

@command("config", help="Display current configuration, and manage additional configurations")
@option("-n", "--new", help="""\b Set an additional configuration
eg. cld config -n <NAME> <CLOUDINARY_URL>""", nargs=2)
@option("-ls", "--ls", help="List all configurations", is_flag=True)
@option("-rm", "--rm", help="Delete an additional configuration", nargs=1)
@option("-url", "--from_url", help="Create a configuration from a Cloudinary URL", nargs=1)
def config(new, ls, rm, from_url):
    if not (new or ls or rm or from_url):
        print('\n'.join(["{}:\t{}".format(k, v if k != "api_secret" else "***************{}".format(v[-4:])) for k, v in cloudinary._config.__dict__.items()]))
        exit(0)

    with open(CLOUDINARY_CLI_CONFIG_FILE, "r+") as f:
        fi = f.read()
        cfg = loads(fi) if fi != "" else {}
        f.close()
    if new:
        try:
            cloudinary._config._parse_cloudinary_url(new[1])
            cfg[new[0]] = new[1]
            api.ping()
            with open(CLOUDINARY_CLI_CONFIG_FILE, "w") as f:
                f.write(dumps(cfg))
                f.close()
            print("Config '{}' saved!".format(new[0]))
        except Exception as e:
            print(e)
            print("Invalid Cloudinary URL: {}".format(new[1]))
            exit(1)
        exit(0)
    if ls:
        print("\n".join(cfg.keys()))
        exit(0)
    if rm:
        if rm not in cfg.keys():
            print("Configuration '{}' not found.".format(rm))
            exit(1)
        del cfg[rm]
        open(CLOUDINARY_CLI_CONFIG_FILE, "w").write(dumps(cfg))
        print("Configuration '{}' deleted".format(rm))
        exit(0)
    if from_url:
        if "CLOUDINARY_URL=" in from_url:
            from_url = from_url[15:]
        try:
            cloudinary._config._parse_cloudinary_url(from_url)
            cfg[cloudinary._config.cloud_name] = from_url
            api.ping()
            with open(CLOUDINARY_CLI_CONFIG_FILE, "w") as f:
                f.write(dumps(cfg))
                f.close()
            print("Config '{}' saved!".format(from_url))
        except Exception as e:
            print(e)
            print("Invalid Cloudinary URL: {}".format(from_url))
            exit(1)
        exit(0)