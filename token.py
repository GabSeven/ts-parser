import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

for id in range(0, 20):
    palavra_decode = encoding.decode([id])
    print(f"Palavra do ID {id}: '{palavra_decode}'")