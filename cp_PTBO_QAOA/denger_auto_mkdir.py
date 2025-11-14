import os
import qaoa
import json
import networkx as nx

if __name__ == "__main__":
    #log
    # 11/9
    #out_file_name = "Neldermead_Parameters_4"
    #graph_file_name = ["regular/regular_3/8","regular/regular_3/10","regular/regular_3/12","regular/regular_3/14","regular/regular_3/16","regular/regular_3/18"]

    # 11/10
    #out_file_name = "all_search"
    #graph_file_name = ["regular/regular_3/8","regular/regular_3/10","regular/regular_3/12","regular/regular_3/14","regular/regular_3/16","regular/regular_3/18"]
    #

    #out_file_name = "Neldermead_Parameters_8_PTBO_2"
    #graph_file_name = ["regular/regular_3/8","regular/regular_3/10","regular/regular_3/12","regular/regular_3/14","regular/regular_3/16","regular/regular_3/18"]
    #out_file_name = "Neldermead_Parameters_8_PTBO_2"
    #graph_file_name_list = ["random/random_7/8","random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]
    #out_file_name = "Neldermead_Parameters_8"
    #graph_file_name_list = ["random/random_7/8","random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]
    

    # 11/11
    #out_file_name = "Neldermead_Parameters_2_speedupPQC"
    #graph_file_name_list = ["regular/regular_3/8","regular/regular_3/10","regular/regular_3/12","regular/regular_3/14","regular/regular_3/16","regular/regular_3/18"]


    #out_file_name = "all_search"

    #out_file_name = "CG_Parameters_8_aizu" #手法、パラメータ数,計算機
    #out_file_name = "Nelder-Mead_Parameters_8_aizu" #手法、パラメータ数,計算機
    #out_file_name = "Powell_Parameters_8_aizu" #手法、パラメータ数,計算機

    #out_file_name = "CG_Parameters_8_PTBO_2_aizu" #手法、パラメータ数,計算機
    #out_file_name = "Nelder-Mead_Parameters_8_PTBO_2_aizu" #手法、パラメータ数,計算機
    out_file_name = "_Parameters_8_PTBO_2_aizu" #手法、パラメータ数,計算機
    graph_file_name_list = ["random/random_7/8","random/random_7/9","random/random_7/10","random/random_7/11","random/random_7/12"] #,"regular/regular_3/10","regular/regular_3/12"]#"regular/regular_3/14"]#,"regular/regular_3/16","regular/regular_3/18"]
    for graph_file_name in graph_file_name_list:
        # 入力 ・出力のベースディレクトリ
        input_dir = os.path.join("in", graph_file_name)
        output_dir = os.path.join("out", out_file_name, graph_file_name)
        os.makedirs(output_dir, exist_ok=True)

        for number in range(300):
            # 入力ファイルパス
            input_path = os.path.join(input_dir, f"{number}in.json")
            output_path = os.path.join(output_dir, f"{number}out.json")
            
            if not os.path.exists(input_path):
                print(f"⚠️ Skipped: {input_path} (not found)")
                continue

            Record = {} #failの生成だけを行う場合

            # 結果を保存
            with open(output_path, 'w') as f:
                json.dump(Record, f, ensure_ascii=False)

            print(f"✅ Saved: {output_path}")
