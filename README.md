## _Naïve_ DNSPod DDNS tool

### Usage

#### Command line

Execute the script with **Python3** with `config.json` and arguments properly provided.

Command arguments:

> `-h`: Show this message and quit, ignoring other arguments
>
> `-c`: Specify the **PATH** of file `config.json`. Default: current working directory
>
> `-I`: Specify the new IP. Default: standard input (syntax unchecked)
>
> `-i`: Enter Python interactive mode after execution

**Note** 

 - If `config.json` is not found, then `config_template.json` will be created. Necessary configuration data is provided **below**.

 - If `-I` is not provided, one can pipe the IP from other command to the script. i.e.

   ``` Bash
   <other command> | ./ddns.py
   ```

---

#### Script

Functions provided:

 - `get_records_list(config)`
   Returns all `A` records.
 - `get_record_info(config)`
   Returns `A` record with specified `subdomain`.
 - `update(new_ip, config)`
   Update new IP.

`config` should be a `dict` containing keys `login_token`, `domain` and `subdomain`.

---

_The script is assumed to be executed in *nix environment._

_More features may be added later on. ;)_

