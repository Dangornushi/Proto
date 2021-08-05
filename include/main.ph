fn print(print_word):
    put(print_word);
    put("\n");
    return True;
end;

fn putchr(put_str):
    put(put_str[1]);
    return True;
end;

fn puts(puts_str):
    put(puts_str[0]);
    put("\n");
    return True;
end;
