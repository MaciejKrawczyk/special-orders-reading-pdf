import PyPDF2


FIRST_WORD_IN_PDF = 'BESTELLDETAILS'
POSITION_BEFORE_MACHINE_PARAMS = 'NO. Ø RINGBREITE RINGHÖHE WRA ERA WRI ERI KBB OEA OBLIQUE'
POSITION_BEFORE_GOLD_TYPES = 'EDELMETALL'


class TrendsellerPDF:
    def __init__(self, nr_pdf):
        self.nr_pdf = nr_pdf
        text_of_pdf_pages_dict = {}
        rings_and_their_pages = {}
        reader = PyPDF2.PdfReader("\\\\10.0.0.5\\public\\MAGDA\\TRENDSELLER\\" + self.nr_pdf)
        for x, page in enumerate(reader.pages):
            text_of_pdf_pages_dict[f'page_{x}'] = page.extract_text().split("\n")
        ring_counter = 0
        for page_number, page in enumerate(text_of_pdf_pages_dict.values()):
            if page[0] == FIRST_WORD_IN_PDF:
                ring_counter += 1
                rings_and_their_pages[f'RING_{ring_counter}'] = (f'page_{page_number}',)
            else:
                rings_and_their_pages[f'RING_{ring_counter}'] += (f'page_{page_number}',)
        # print(rings_and_their_pages)
        # print(text_of_pdf_pages_dict)
        self.rings_and_their_pages = rings_and_their_pages
        self.text_of_pdf_pages_dict = text_of_pdf_pages_dict

    def get_number_of_rings_in_pdf(self):
        print(len(self.rings_and_their_pages))
        return len(self.rings_and_their_pages)

    # --------------------------------------------- specific parameters

    def get_profile_and_params(self):
        data = {}
        for ring, pages in self.rings_and_their_pages.items():
            page_text = self.text_of_pdf_pages_dict[f'{pages[0]}']
            index_of_params = page_text.index(POSITION_BEFORE_MACHINE_PARAMS)
            tab_with_params = page_text[index_of_params + 1].split()
            profile = tab_with_params[0]
            r51 = tab_with_params[2]
            r52 = tab_with_params[3]
            r60 = tab_with_params[4]
            r40 = tab_with_params[5]
            r61 = tab_with_params[6]
            r41 = tab_with_params[7]
            r20 = tab_with_params[8]
            data[f'{ring}'] = {'profile': f'{profile}', 'r51': f'{r51}', 'r52': f'{r52}', 'r60': f'{r60}',
                               'r40': f'{r40}', 'r61': f'{r61}', 'r41': f'{r41}', 'r20': f'{r20}'}
        print(data)
        return data

    def has_stones(self):
        data = {}
        for ring, pages in self.rings_and_their_pages.items():
            if len(pages) > 1:
                data[f'{ring}'] = True
            else:
                data[f'{ring}'] = False
        print(data)
        return data

    def get_material_type_width_height(self):
        data = {}
        for ring, pages in self.rings_and_their_pages.items():
            page_text = self.text_of_pdf_pages_dict[f'{pages[0]}']
            index_before_gold_types = page_text.index(POSITION_BEFORE_GOLD_TYPES)
            tab_with_color_type = page_text[index_before_gold_types + 1].split()[1:]
            tab_with_width = page_text[index_before_gold_types + 2].split()[1:]
            tab_with_height = page_text[index_before_gold_types + 3].split()[1:]
            loop_counter_width_height = 0
            loop_counter_type = 1
            tab_type_good = []
            tab_colors_good = []
            tab_width_good = []
            tab_height_good = []
            if len(tab_with_color_type) % 2 == 1:
                tab_with_color_type.pop()
            for position in range(0, len(tab_with_color_type), 2):
                tab_colors_good.append(tab_with_color_type[position])
                tab_width_good.append(tab_with_width[loop_counter_width_height])
                tab_height_good.append(tab_with_height[loop_counter_width_height])
                tab_type_good.append(tab_with_color_type[loop_counter_type][:-2])
                loop_counter_width_height += 1
                loop_counter_type += 2
            for i in range(len(tab_colors_good) - 1):
                if tab_colors_good[i] == tab_colors_good[i + 1]:
                    tab_colors_good.pop(i + 1)
                    tab_type_good.pop(i + 1)
                    tab_height_good.pop(i + 1)
                    temp = tab_width_good[i + 1]
                    tab_width_good.pop(i + 1)
                    tab_width_good[i] = float(tab_width_good[i]) + float(temp)
            data[f'{ring}'] = {}
            for j in range(len(tab_colors_good)):
                data[f'{ring}'][f'COLOR_{j}'] = {}
                data[f'{ring}'][f'COLOR_{j}']['color'] = tab_colors_good[j]
                data[f'{ring}'][f'COLOR_{j}']['type'] = tab_type_good[j]
                data[f'{ring}'][f'COLOR_{j}']['width'] = tab_width_good[j]
                data[f'{ring}'][f'COLOR_{j}']['height'] = tab_height_good[j]
        print(data)
        return data


if __name__ == "__main__":
    trendseller = TrendsellerPDF("Trendseller33460.pdf")
    # trendseller.get_number_of_rings_in_pdf()
    # trendseller.get_profile_and_params()
    # trendseller.has_stones()
    trendseller.get_material_type_width_height()