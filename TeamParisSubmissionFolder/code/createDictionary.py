def main():
  with open("../data/corpus/corpus.txt") as f:
    content = f.readlines()
    wordSet = set()
    for line in content:
      words = line.split()
      wordSet.update(words)

    dictionary = open('../data/dicitonary.txt','w')
    for word in wordSet:
      dictionary.write(word + ":\n")
    print wordSet

# Boilerplate
if __name__ == "__main__":
  main();