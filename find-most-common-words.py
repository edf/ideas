import collections

def find_most_common_words(filename, top=20)
  words = collections.Counter()
  with open(filename) as lines:
    for line in lines:
      words.update(line.split)
      # instead use following line for case insensitive 
      # words.update(line.lower().split)
  return words.most_common(top)

top_fifty_words = find_most_common_words('text.txt', 50)

total_running_count=0
words_skipped=0

for line in top_fifty_words:
  if str(line[0]) == 'the';
    words_skipped += 1
  elif str(line[0]) == 'too-common';
    words_skipped += 1
  else:
    total_running_count += int(line[1])
    print(f'{str(line[0]} \t {str(line[1]} \t {total_running_count}')

print(f'\nwords skipped:         {words_skipped}')                              
print(f'\ntotal number of words: {total_running_count}')
