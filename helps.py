import os

class Option_Commandlines:
    def __init__(self, word):
        self.ops = word

    def options(self):
        
        if self.ops == "-h" or self.ops == "--helps":
            self.help()

        elif self.ops == "-w" or self.ops == "--where":
            self.where()
        
        elif self.ops.startswith("-"):
            print("OptionErr : 不明なコマンドです / helpコマンドを参考にしてください")
        
        elif self.ops == "helloworld":
            print("ようこそ！")
            return False

        else:
            return True
    
    def help(self):
        pw = """
        コマンド管理番号2 : helpコマンド[ --help, -h ]

    コマンド管理番号                 オプション形式                            内容
        01           python3 compile.py, ./proto [filename]    protoインタプリタ起動m、コード実行

        02                      -h, --help                         helpメニューの表示
        
        03                      -w, --where                      実行ファイルの場所を表示
        """
        print(pw)
    
    def where(self):
        print("       コマンド管理番号3 : whereコマンド[ --where, -w ]\n実行ファイル : "+os.getcwd()+"/"+__file__)

if __name__ == '__main__':
    OC = Option_Commandlines("main.pr")
    if OC.options():
        print("OK")
    