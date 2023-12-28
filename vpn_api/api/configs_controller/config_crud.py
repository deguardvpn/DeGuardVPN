from utils.create_conf import main
import requests


def create_user_config(user_id: str):
    config = main(user_id)
    return config


def delete_configs(user_ids: list):
    with open('../../../config/wg_confs/wg0.conf', 'r') as f:
        wg0_conf = f.read()

    print(wg0_conf)

    for user_id in user_ids:

        target_start = f'#NP {user_id}'
        target_end = f'# {user_id}'

        if wg0_conf.count(target_start) > 1:
            while wg0_conf.count(target_start) != 0:
                target_start = f'#NP {user_id}'
                target_end = f'# {user_id}'

                start, end = wg0_conf.find(target_start), wg0_conf.find(target_end)

                res = wg0_conf[start:end + 41]

                wg0_conf = wg0_conf.replace(res, '')

            with open('../../../config/wg_confs/wg0.conf', 'w') as f:
                f.write(wg0_conf)

        else:
            start, end = wg0_conf.find(target_start), wg0_conf.find(target_end)

            res = wg0_conf[start:end + 41]
            wg0_conf = wg0_conf.replace(res, '')

            with open('../../../config/wg_confs/wg0.conf', 'w') as f:
                f.write(wg0_conf)

        with open('../../../config/wg_confs/wg0.conf', 'w') as f:
            f.write(wg0_conf)

        print(wg0_conf)

        print("[TASK DONE]")
        # r = requests.get("http://192.168.240.2:8002/api/sync_configs")

    return True


delete_configs("5da60736-6cef-4ab2-849b-2064ae055f34")
