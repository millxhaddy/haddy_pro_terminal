import time
from moomoo import OpenSecTradeContext, TrdMarket, SecurityFirm

print("================================================================")
print("       MENGIMBAS BAKI & AKAUN SEBENAR DI MOOMOO OPEND           ")
print("================================================================")

# Sambung ke OpenD
try:
    ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.US, host="127.0.0.1", port=11111)
    time.sleep(1.5)  # Beri masa OpenD sedia
    
    # 1. Senarai Akaun
    ret, acc_list = ctx.get_acc_list()
    if ret == 0:
        print("\n📋 SENARAI AKAUN DIJUMPAI:")
        print(acc_list[["acc_id", "trd_env", "sim_acc_type"] if "sim_acc_type" in acc_list.columns else ["acc_id", "trd_env"]])
        
        # 2. Uji setiap akaun yang ada
        for idx, row in acc_list.iterrows():
            target_id = int(row["acc_id"])
            print(f"\n---> Mengimbas Dana untuk Acc ID: {target_id}...")
            
            ret_f, df_funds = ctx.get_acc_details(acc_id=target_id)
            if ret_f == 0 and not df_funds.empty:
                print(f"     ✅ Total Assets : {df_funds.get('total_assets', [0])[0]}")
                print(f"     ✅ Cash Balance : {df_funds.get('cash', [0])[0]}")
                print(f"     ✅ Market Val   : {df_funds.get('market_val', [0])[0]}")
                print(f"     ✅ Unrealized PL: {df_funds.get('unrealized_pl', [0])[0]}")
            else:
                print(f"     ⚠️ Status Dana: {df_funds}")

            # 3. Pegangan Saham
            ret_p, df_pos = ctx.get_acc_positions(acc_id=target_id)
            if ret_p == 0 and not df_pos.empty:
                print(f"     📦 Pegangan Saham ({len(df_pos)} kaunter):")
                for _, pr in df_pos.iterrows():
                    print(f"        - {pr.get('code')}: {pr.get('qty')} unit @ ${pr.get('nominal_price')}")
            else:
                print(f"     📦 Tiada saham aktif di Acc ID {target_id}.")
    else:
        print("Ralat get_acc_list:", acc_list)

    ctx.close()

except Exception as e:
    print("Ralat:", e)

print("\n================================================================")