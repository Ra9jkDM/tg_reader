from typing import NamedTuple

class PageSlicer:
    separators = ['.', ',', ' ', '-', '\n']

    def check_is_enough(self, text, start, amount):
        return len(text) - start >= amount

    def slice(self, text, start, amount):
        end = start + amount

        if end >= len(text):
            return SliceDTO(**{'amount': len(text),
                                'text': text[start:]})
        else:
            nearest = self._get_nearest_separator(text, end) + 1
            return SliceDTO(**{'amount': nearest,
                                'text': text[start:nearest]})

    def slice_2_pages(self, text, text_2, start, amount):
        chunk = text[start:]
        chunk_2_len = amount - len(chunk)
        part = self.slice(text_2, 0, chunk_2_len)

        return SliceDTO(**{'amount': part.amount,
                             'text': chunk + "\n" + part.text})


    def current_slice(self, text, start, amount):
        chunk = text[: start]

        chunk = chunk[::-1]
        nearest = self._get_nearest_separator(chunk, amount)
        # print(chunk[::-1], nearest, chunk[:nearest])
        chunk = chunk[:nearest]

        return SliceDTO(**{'amount': start - len(chunk) - 2,
                             'text': chunk[::-1]})

    def previous_slice(self, text, start, amount):
        result = self.current_slice(text, start, amount)
        result = self.current_slice(text, result.amount, amount)

        return SliceDTO(**{'amount': result.amount,
                             'text': result.text})

    def previous_slice_2_pages(self, text, text_2, start, amount):
        pass

    def _get_nearest_separator(self, text, start):
        results = []

        for i in self.separators:
            tmp = text.find(i, start)

            if tmp != -1:
                results.append(tmp)

        return min(results)

    
    def _section(self, text, start, stop):
        return text[start: stop + 1]

class SliceDTO(NamedTuple):
    amount: int
    text: str