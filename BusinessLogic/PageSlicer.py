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
