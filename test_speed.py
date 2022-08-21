import json
import random
import time
from functools import lru_cache
from unidecode import unidecode

import numpy as np
import pandas as pd

from fast_unidecode import unidecode as fast_unidecode

@lru_cache(8)
def py_unidecode(x):
    return unidecode(x)

@lru_cache(8)
def rust_unidecode(x):
    return fast_unidecode(x)

if __name__ == "__main__":
    db = {}
    db["a"] = "看看谁的脚丫子更大，就踩上去"
    db["b"] = "回去以后"
    db["c"] = 14 * "回去以后"
    db["num"] = "100,23"
    db["cur"] = "100,23 CZK"
    db["d"] = " げんまい茶 ᔕᓇᓇ"
    db["e"] = "csonbhxehj"
    db["f"] = "KNFOTVDFLQ"
    db["g"] = "kRAaicQQMzSFtOkZPeyUumzAJoRmjDXJ"
    db["h"] = 5 * "299mm73d28rg6x7m8qe"
    db["i"] = "8LhNr31RxtmUrtWponbl"
    db["j"] = 100 * "8LhNr31RxtmUrtWponbl"
    db["k"] = "}<[,[{<#[/=-'@-%(*&~"
    db["l"] = int(5e4) * "Æneid 1234 098 @#$!@)() -0/'ˇmkdaslllsmdlamdlkas げんまい茶 ᔕᓇᓇ 北亰 étude 四千年前有一个姑娘叫姜嫄，她有一天觉得很空虚，就到郊外玩，看见一只巨人脚印，也许是外星人留下的，她想上去比一比，看看谁的脚丫子更大，就踩上去。踩上去就发现肚子里乱动，跟怀了孕似的。回去以后，肚子里的小孩，又老不出来，过了十二个月才生下来。"
    db["m"] = ".H<ncWi&dY_Wf)`'bNR=P@)G\8EkVEdmTZdMVO]gM2v m!"
    db["n"] = 14 * "aDc4__uu3I_jq/68=YK(=Z'/3u5@{cu5_6{ v]U9q nZ_#X&ZbXBv~tFmb@p}Z"
    

    res_list = []

    for _iters in [1, 5, 10, 20, 100, 500]:
        for _ in range(10):
            RES = {"_iters": _iters}

            for key, _string in db.items():
            
                T = []
                T_rust = []

                iters = 1

                print(key)
                
                iters = min(3, _iters) if key == "l" else _iters

                for _ in range(iters):
                    string = "".join(random.sample(_string, len(_string)))

                    t0 = time.time()
                    _ = py_unidecode(string)
                    T.append(time.time() - t0)
                print(f"Python execution: {1000 * np.mean(T):.3f} ± {1000 * np.std(T):.3f} ms.")

                for _ in range(iters):
                    string = "".join(random.sample(_string, len(_string)))

                    t0 = time.time()
                    _ = fast_unidecode(string)
                    T_rust.append(time.time() - t0)
                print(f"PyO3 execution: {1000 * np.mean(T_rust):.3f} ± {1000 * np.std(T_rust):.3f} ms.")

                if np.mean(T) > np.mean(T_rust):
                    print(f"Speedup: {np.mean(T) / np.mean(T_rust):.2f}x.")
                else:
                    print(f"Slowdown: {np.mean(T_rust) / np.mean(T):.2f}x.")

                speedup = np.mean(T) / np.mean(T_rust)
                speedup = 1.0 if speedup == float("inf") else speedup
                speedup = 1.0 if speedup == float("nan") else speedup
                speedup = 1.0 if speedup == 0.0 else speedup
                RES[key] = round(speedup, 4)

                print("===========")

            py_unidecode.cache_clear()
            rust_unidecode.cache_clear()
            res_list.append(RES)

    df = pd.DataFrame(res_list)
    df.to_csv("result.tsv", sep="\t", index=None)

    print(df)

    better = (df.drop("_iters", axis=1) > 1.0).sum().sum()
    worse = (df.drop("_iters", axis=1) < 1.0).sum().sum()
    average = df.drop("_iters", axis=1).mean().mean()

    print(f"Rust outperforms on {100 * better / (better + worse):.2f}%.")
    print(f"Average speed-up {average:.2f}x.")