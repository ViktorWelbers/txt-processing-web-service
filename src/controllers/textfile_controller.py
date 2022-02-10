from src.models.textline_models import OneLiner,AdditionalOneLiner,LongestHundredLines,TwentyLongestLines
import random
from src.controllers.util.file_util import get_file_folder, most_frequent_char, reverse_string
import os
from pathlib import Path
from dicttoxml import dicttoxml
from typing import Union, List, Tuple, TextIO
from fastapi import HTTPException


class ControllerBase():

    @staticmethod
    def get_last_upload()-> Path:
        try:
            return max(Path(get_file_folder()).glob('*/'), key=os.path.getmtime)
        except:
            raise HTTPException(status_code=400, detail="No File was uploaded yet")


class OneLineController(ControllerBase):

    @staticmethod
    def __convert_to_content_type(data: OneLiner,accept: str):
        if accept == "application/*" or accept == "application/json":
            return data.json()
        elif accept == "text/plain":
            return data.random_line
        elif accept == "application/xml":
            return dicttoxml(data.dict())

    def get_random_line(self)-> Tuple[TextIO,List[str],str]:
        file = open(self.get_last_upload(), 'r')
        all_lines = file.readlines()
        if len(all_lines) < 1:
            raise HTTPException(status_code=400, detail="file that is uploaded cannot be empty")
        return file, all_lines, random.choice(all_lines)

    def one_random_line_logic(self, accept: str, backwards: bool = False)-> Union[dict,str]:
        file, all_lines,random_line = self.get_random_line()
        selected_line = random_line.replace('\n', '')
        if backwards:
            selected_line= reverse_string(selected_line)
        if accept != "application/*":
            return self.__convert_to_content_type(
                data = OneLiner(random_line = selected_line),
                accept=accept)
        most_frequent = most_frequent_char(random_line)[0] if len(random_line) != 0 else "empty line"
        return self.__convert_to_content_type(
                        data = AdditionalOneLiner(random_line=selected_line,
                                                    line_number = all_lines.index(random_line) + 1,
                                                    file_name = Path(file.name).stem.split('_____')[1] + ".txt",
                                                    most_common = most_frequent),
                        accept = accept)


class MultipleLineController(ControllerBase):

        @staticmethod
        def __iterate_through_file(file):
            with open(file) as f:
                return([line.rstrip('\n') for line in f])

        def longest_hundred_lines(self) -> LongestHundredLines:
            all_lines = []
            for file in get_file_folder().iterdir():
                all_lines.extend(self.__iterate_through_file(file))
            sorted_lines = sorted(all_lines, key=len, reverse=True)
            x = sorted_lines[:99]
            return LongestHundredLines(lines = sorted_lines[:99])

        def twenty_longest_one_file(self) -> TwentyLongestLines:
            all_lines = self.__iterate_through_file(self.get_last_upload())
            sorted_lines = sorted(all_lines, key=len, reverse=True)
            return TwentyLongestLines(lines = sorted_lines[:20])


multiple_line_controller = MultipleLineController()
random_line_controller = OneLineController()

