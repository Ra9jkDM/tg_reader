import unittest

from BusinessLogic.PageSlicer import PageSlicer

text = '''Парк станочного оборудования, оснащенного ЧПУ, огромен и разнообразен. 
Достаточно перечислить лишь самые основные: это токарные, фрезерные, шлифовальные, 
металлорежущие, сверлильные станки, которые подразделяются на множество типов 
и модификаций. Сложное и многообразное производство требует такого же сложного 
оборудования. Однако, при всем многообразии типов и моделей принцип работы станков 
с ЧПУ сводится к наличию программного обеспечения, задающего алгоритм работы станка.
Станки с ЧПУ не требует высокой квалификации специалиста - станочника, достаточно обучить
 персонал приемам управления программой. Станки с ЧПУ – это современное оборудование, 
 позволяющее обеспечить высокую производительность труда при отменном качестве производимых 
 работ. Использование таких станков значительно повышает общий уровень культуры производства.'''

text_2 = '''Фрезерные станки — группа металлорежущих и деревообрабатывающих станков в 
классификации по виду обработки. Фрезерные станки предназначены для обработки с помощью 
фрезы плоских и фасонных поверхностей, зубчатых колёс и т. п., металлических и других 
заготовок. При этом фреза, закрепленная в шпинделе фрезерного станка, совершает вращательное 
движения (главное движение), а заготовка, закреплённая на столе, остаётся неподвижной. 
Управление может быть ручным, автоматизированным или осуществляться с помощью системы ЧПУ. '''

class TestPageSlicer(unittest.TestCase):
    def setUp(self):
        self.slicer = PageSlicer()

    def test_get_first_slice(self):
        chunk = self.slicer.slice(text, 0, 60).text

        self.assertEqual(chunk, "Парк станочного оборудования, оснащенного ЧПУ, огромен и разнообразен.")

    def test_get_middle_slice(self):
        chunk = self.slicer.slice(text, 100, 80).text

        self.assertEqual(chunk, "самые основные: это токарные, фрезерные, шлифовальные, \nметаллорежущие, сверлильные ")

    def test_get_last_slice(self):
        chunk = self.slicer.slice(text, 802, 80).text

        self.assertEqual(chunk, "повышает общий уровень культуры производства.")

    def test_get_two_slice(self):
        result = self.slicer.slice(text, 350, 80)
        result = self.slicer.slice(text, result.amount, 40)

        self.assertEqual(result.text, "обеспечения, задающего алгоритм работы станка.")

    def test_is_enough_true(self):
        result = self.slicer.check_is_enough("a"*10, 0, 5)

        self.assertTrue(result)
    
    def test_is_enough_length_equal_true(self):
        result = self.slicer.check_is_enough("a"*10, 5, 5)

        self.assertTrue(result)

    def test_is_enough_flase(self):
        result = self.slicer.check_is_enough("a"*10, 6, 5)

        self.assertFalse(result)

    def test_slice_2_pages(self):
        result = self.slicer.slice_2_pages(text, text_2, 825, 100)

        self.assertEqual(result.text, "культуры производства.\nФрезерные станки — группа металлорежущих и деревообрабатывающих станков в \nклассификации ")

    def test_slice_2_pages_and_get_next_slice(self):
        result = self.slicer.slice_2_pages(text, text_2, 825, 100)
        result = self.slicer.slice(text_2, result.amount, 40)

        self.assertEqual(result.text, "по виду обработки. Фрезерные станки предназначены ")

    def test_current_slice(self):
        amount = 36
        result1 = self.slicer.slice(text, 16, amount)
        result2 = self.slicer._previous_slice(text, result1.amount, amount)

        self.assertEqual(result2.text, result1.text)

    def test_current_slice_2(self):
        amount = 100
        result1 = self.slicer.slice(text, 83, amount)
        result2 = self.slicer._previous_slice(text, result1.amount, amount)

        self.assertEqual(result2.text, result1.text)

    def test_previous_slice(self):
        amount = 36
        result1 = self.slicer.slice(text, 16, amount)
        result2 = self.slicer.slice(text, result1.amount, amount)

        # get current slice
        result3 = self.slicer.previous_slice(text, result2.amount, amount, len(result2.text))
        result4 = self.slicer.previous_slice(text, result3.amount, amount)

        self.assertEqual(result4.text, result1.text)

    def test_get_first_slice(self):
        result = self.slicer.previous_slice(text, 5, 10)

        self.assertEqual(result.text, "Парк ")

    def test_previous_slice_2(self):
        amount = 55
        result1 = self.slicer.slice(text, 106, amount)
        result2 = self.slicer.slice(text, result1.amount, amount)

        result3 = self.slicer.previous_slice(text, result2.amount, amount, len(result2.text))
        result4 = self.slicer.previous_slice(text, result3.amount, amount)

        # Из-за особенностей реализации
        self.assertEqual("основные: "+result4.text+result3.text, result1.text+result2.text)

    def test_previous_slice_3(self):
        amount = 36
        result1 = self.slicer.slice(text, 16, amount)
        result2 = self.slicer.slice(text, result1.amount, amount)
        result3 = self.slicer.slice(text, result2.amount, amount)
        result4 = self.slicer.slice(text, result3.amount, amount)
        result5 = self.slicer.slice(text, result4.amount, amount)

        result_1 = self.slicer.previous_slice(text, result5.amount, amount, len(result5.text))
        result_2 = self.slicer.previous_slice(text, result_1.amount, amount)
        result_3 = self.slicer.previous_slice(text, result_2.amount, amount)
        result_4 = self.slicer.previous_slice(text, result_3.amount, amount)

        # Из-за особенностей реализации
        self.assertEqual(result2.text[2:], result_4.text[:-5])

    def test_previous_slice_2_pages(self):
        result = self.slicer.previous_slice_2_pages(text, text_2, 10, 20)

        self.assertEqual(result.text, "производства.")

    def test_is_enough_previous_true(self):
        result = self.slicer.check_is_enough_previous("a"*10, 5, 5)

        self.assertTrue(result)
    
    def test_is_enough_previous_false(self):
        result = self.slicer.check_is_enough_previous("a"*10, 4, 5)

        self.assertFalse(result)

    def test_workflow(self):
        start = 40
        amount = 30

        if self.slicer.check_is_enough(text, start, amount):
            self.slicer.slice(text, start, amount)
        else:
            self.slicer.slice_2_pages(text, text_2, start, amount)


if __name__ == "__main__":
    unittest.main()


# python -m Tests.BusinessLogic.TestPageSlicer