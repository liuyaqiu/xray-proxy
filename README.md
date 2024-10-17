## Start a XRAY reality proxy

```bash
./start.sh
```

## dependency
Please add the `.env` file inside this directory, it should contain:
```
PROXY_LINK={proxy_url}
WG_PORT={wireguard_port}
```

This script will do the following thing:
1. Download the xray binary into path `xray-bin`, if it already exists, skip.
2. generate the xray config file `config_client.json`.
3. launch the xray proxy client process.

## hint
You could download the xray binary from [xray release](https://github.com/XTLS/Xray-core/releases) by yourself, and extract it into `xray-bin`.

Please confirm that the `{wireguard_port}` is equal to your wireguard client config.

