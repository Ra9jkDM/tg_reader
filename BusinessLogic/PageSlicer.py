from typing import NamedTuple

class PageSlicer:
    separators = ['.', ',', ' ', '-', '\n']

    def check_is_enough(self, text, start, amount):
        return len(text) - start >= amount

    def check_is_enough_previous(self, text, start, amount):
        return start >= amount

    def slice(self, text, start, amount):
        if len(text) > start + amount:
            end = self._get_nearest_separator(text, start + amount) + 1
        else:
            end = len(text)

        return SliceDTO(**{'amount': end,
                            'text': text[start: end]})

    def slice_2_pages(self, text, text_2, start, amount):
        chunk = text[start:]
        chunk_2_len = amount - len(chunk)
        part = self.slice(text_2, 0, chunk_2_len)

        return SliceDTO(**{'amount': part.amount,
                             'text': chunk + "\n" + part.text})


    def _previous_slice(self, text, start, amount):
        text = text[start-1::-1]
        end = self._get_nearest_separator(text, amount) - 1

        text = text[end::-1]
        return SliceDTO(**{'amount': start-len(text),
                            'text': text})

    def previous_slice(self, text, start, amount, current_text_size = -1):
        """Возвращает значения не идентичные значениям, полученным при нарезании текста вперед, т.к. 
        не знает точной длинны предыдущего отрезка. Зависимость бага от: союзов, предлогов и длинных слов.
        Для того, чтобы пользователю корректно отображался предыдущий отрывок текста нужно передать
        длину текущего отрезка - {current_text_size}"""
        if current_text_size != -1:
            result = self._previous_slice(text, start, current_text_size)
        else:
            result = self._previous_slice(text, start, amount)

        return SliceDTO(**{'amount': result.amount,
                             'text': result.text})

    def previous_slice_2_pages(self, text, text_2, start, amount):
        chunk = text_2[:start]
        chunk_2_len = len(chunk)

        return self.previous_slice(text, len(text), chunk_2_len)
        

    def _get_nearest_separator(self, text, start):
        results = []

        for i in self.separators:
            tmp = text.find(i, start)

            if tmp != -1:
                results.append(tmp)

        if len(results) > 0:
            return min(results)
        return 0

    

class SliceDTO(NamedTuple):
    amount: int
    text: str


separators = ['.', ',', ' ', '-', '\n']

def slice(text, start, amount):
    end = start+amount
    return SliceDTO(**{'amount': end,
                        'text': text[start: end]})
    
def previous_slice(text, start, amount):
    end = start-amount
    return SliceDTO(**{'amount': end,
                        'text': text[end: start]})

def _get_nearest_separator(text, start):
        results = []

        for i in separators:
            tmp = text.find(i, start)

            if tmp != -1:
                results.append(tmp)

        
        if len(results) > 0:
            return min(results)
        return 0

def slice_sep(text, start, amount):
    print(start, amount, len(text))
    if len(text) > start + amount:
        end = _get_nearest_separator(text, start+amount) + 1
    else:
        end = len(text)
        print(-1)
    return SliceDTO(**{'amount': end,
                        'text': text[start: end]})

def previous_slice_sep(text, start, amount):
    text = text[start-1::-1]
    print(text, start)
    end = _get_nearest_separator(text, amount) - 1
    print("end", end)
    text = text[end::-1]
    return SliceDTO(**{'amount': start-len(text),
                        'text': text})

if __name__ == "__main__":
    text = "0123456789"
    start = 0
    amount = 3
    print(text[0:3])
    print(text[3:6])

    r = slice(text, 0, 3)
    print(r)
    r = slice(text, r.amount, amount)
    print(r)

    p = previous_slice(text, r.amount, amount)
    print(p)
    p = previous_slice(text, p.amount, amount)
    print(p)

    text = "123 456 789 0"
    t = _get_nearest_separator(text, amount)
    print(t)
    r = slice_sep(text, 0, amount)
    print(r)
    r = slice_sep(text, r.amount, amount)
    print(r)
    r = slice_sep(text, r.amount, amount)
    print(r)
    rx = slice_sep(text, r.amount, amount)
    print(rx)

    p = previous_slice_sep(text, r.amount, amount)
    print(p)
    p = previous_slice_sep(text, p.amount, amount)
    print(p)
    p = previous_slice_sep(text, p.amount, amount)
    print(p)
    # print(text[-1::-1])

