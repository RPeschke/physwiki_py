from physwiki.pyMarkdown import set_Env, get_Env



class lineNR_T:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return str(get_Env("line"))
    
__line__ = lineNR_T()