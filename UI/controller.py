import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return
        anno = int(self._view.ddyear.value)
        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.create_alert("Selezionare una shape!")
            return
        shape = self._view.ddshape.value
        self._view.txt_result1.controls.clear()
        self._model.crea_grafo(anno, shape)
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {len(self._model.grafo.nodes)}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di edges: {len(self._model.grafo.edges)}"))
        self._view.txt_result1.controls.append(ft.Text(f"--- top 5 edges ---"))
        for str in self._model.get_top_edges():
            self._view.txt_result1.controls.append(ft.Text(f"{str}"))

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fill_ddyear(self):
        years = self._model.get_years()
        self._view.ddyear.options.clear()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(f"{y}"))

    def fill_ddshape(self, e):
        anno = int(self._view.ddyear.value)
        self._view.ddshape.options.clear()
        self._view.ddshape.value = None
        shapes = self._model.get_shapes_year(anno)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        self._view.update_page()
