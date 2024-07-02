import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        nodi,archi = self._model.graphDetails()
        self._view.txt_result.controls.append(ft.Text(f"GRAFO CREATO CORRETTAMENTE CON {nodi} NODI E {archi} ARCHI "))


        self._view.update_page()
    def handleCompConnessa(self,e):
        try:
            testo = int(self._view._txtIdOggetto.value)
        except ValueError:
            self._view.create_alert("ERRORE NON VALIDO L'ELEMENTO INSERITO")
            return
        self._numeroCom= 0

        for u in self._model._grafo.nodes:
            if u.object_id == testo:
                self._view.txt_result.controls.append(ft.Text(f"L'OGGETTO E' PRESENTE NEL GRAFO"))
                componente,numero = self._model.getComponente(testo)
                self._numeroCom= numero
                for c in componente:
                    self._view.txt_result.controls.append(ft.Text(f"{c.object_id}"))


        self._view._ddLun.disabled= False
        for i in range(2, self._numeroCom+1):
            self._view._ddLun.options.append(ft.dropdown.Option(i))

        self._view._btnCercaPercorso.disabled = False
        self._view.update_page()



    def handleCercaPercorso(self,e):
        if self._view._ddLun.value== "" or self._view._ddLun.value ==None:
            return self._view.create_alert("ERRORE PRIMA INSERIRE UN NUMERO")
        valore = self._view._ddLun.value
        nodo = int(self._view._txtIdOggetto.value)
        print(nodo)
        percorso, pesoMax = self._model.getPath(valore,nodo)
        self._view.txt_result.controls.append(ft.Text(f"il percorso ha peso {pesoMax}"))
        self._view.update_page()


