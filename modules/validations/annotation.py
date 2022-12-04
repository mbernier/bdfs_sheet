import sys
from typing import TypeVar, List
from inspect import signature, Parameter


Typevar_List_Str = TypeVar("Typevar_List_Str", list, str)

class Validation_Annotation():

    @staticmethod
    def getValidations(methodSignature, key:str) -> list:

        print(key)
        # print(methodSignature)

        #get the annotation property from the methodSignature
        field_annotation = methodSignature[key].annotation

        # print(field_annotation)

        annotation_list = Validation_Annotation.setup(field_annotation)

        # print(annotation_list)

        clean_annotations = Validation_Annotation.cleanAnnotationList(annotation_list)

        # print(clean_annotations)
        return clean_annotations


    # turn whatever validations we get into a list
    @staticmethod
    def setup(field_annotations: Typevar_List_Str) -> list:

        annotation_list = field_annotations

        if field_annotations is str:
             annotation_list = [field_annotations]

        return annotation_list


    @staticmethod
    def cleanAnnotationList(annotation_list:list) -> list:
        clean_annotations = []
        for annotation in annotation_list:
            # print(annotation)
            clean_annotations.append(Validation_Annotation.clean(annotation))
        return clean_annotations

    @staticmethod
    def clean(annotation):
        if annotation.__name__ == "_empty":
            return None

        return annotation.__name__