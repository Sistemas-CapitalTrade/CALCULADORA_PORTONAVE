from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QDateEdit, QPushButton, QGroupBox, QLabel, QSpacerItem, QSizePolicy, QWidgetAction, QCheckBox, QCalendarWidget, QToolButton, QMenu, QScrollArea
)
from PySide6.QtCore import Qt, QDate, QEvent
from PySide6.QtGui import QPalette, QBrush, QPixmap, QFont, QAction
import sys

class CustomDateEdit(QDateEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCalendarPopup(True)
        self.calendarWidget().setStyleSheet(self.get_calendar_style())
        self.calendarWidget().installEventFilter(self)

    def get_calendar_style(self):
        return """
            QCalendarWidget {
                background-color: rgba(255, 255, 255, 0.25); /* Fundo do calendário */
                color: white;
            }
            QCalendarWidget QAbstractItemView {
                background-color: rgba(255, 255, 255, 0.25); /* Fundo dos itens */
                color: white;
                selection-background-color: rgba(255, 255, 255, 0.35); /* Fundo quando selecionado */
                selection-color: black; /* Cor do texto quando selecionado */
            }
            QCalendarWidget QAbstractItemView::item {
                background-color: rgba(255, 255, 255, 0.25); /* Fundo dos itens */
                color: white;
            }
            QCalendarWidget QAbstractItemView::item:hover {
                background-color: rgba(255, 255, 255, 0.35); /* Fundo dos itens ao passar o mouse */
                color: black; /* Cor do texto ao passar o mouse */
            }
            QCalendarWidget QAbstractItemView::item:selected {
                background-color: rgba(255, 255, 255, 0.35); /* Fundo dos itens quando selecionado */
                color: black; /* Cor do texto quando selecionado */
            }
            QCalendarWidget QToolButton {
                background-color: rgba(255, 255, 255, 0.25); /* Fundo dos botões */
                color: white;
                border: none;
            }
            QCalendarWidget QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.35); /* Fundo dos botões ao passar o mouse */
            }
            QCalendarWidget QToolButton:pressed {
                background-color: rgba(255, 255, 255, 0.35); /* Fundo dos botões ao clicar */
            }
        """

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.Show and source is self.calendarWidget():
            source.setFixedWidth(self.width())  # Ajusta a largura do calendário quando o pop-up é mostrado
        return super().eventFilter(source, event)

class StorageCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CALCULADORA DE ARMAZENAGEM")
        self.resize_to_full_screen()
        self.set_background_image()
        self.selected_options_values = {}  # Dicionário para armazenar valores correspondentes

        # Layouts principais
        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        # Título
        title_label = QLabel("CALCULADORA DE ARMAZENAGEM")
        title_label.setFont(QFont("Arial", 42, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title_label)

        # # Widgets com rótulos
        entrada_container_label = QLabel("ENTRADA DO CONTÊINER:")
        saida_container_label = QLabel("SAÍDA DO CONTÊINER:")

        # # Ajuste de estilo dos rótulos
        for label in [entrada_container_label, saida_container_label]:
            label.setStyleSheet("color: white;")

        # Widgets
        select_recinto = self.create_combobox_recinto("SELECIONE O RECINTO")
        valor_cif = self.create_lineedit_CIF("VALOR DE CIF EM R$")
        select_tipo_mercadoria = self.create_combobox_mercadoria("SELECIONE O TIPO DA MERCADORIA")
        self.entrada_container = self.create_dateedit()
        self.saida_container = self.create_dateedit()
        self.periodo_armazenagem = self.create_combobox_armazenagem("PERÍODO DE ARMAZENAGEM")
        custos = self.create_combobox("CUSTOS")
        gerar_simulacao = self.create_button("GERAR SIMULAÇÃO", is_action_button=True)
        salvar_pdf = self.create_button("GERAR PDF", is_action_button=True)

        # Layout de parâmetros de simulação
        simulacao_group = QLabel("SIMULAÇÃO DA ARMAZENAGEM")
        simulacao_group.setFont(QFont("Arial", 16))

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 16))
        self.result_label.setStyleSheet("color: white; background-color: rgba(255, 255, 255, 0.1); padding: 10px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setVisible(False)  # Oculta inicialmente

        self.result_label_levante = QLabel("")
        self.result_label_levante.setFont(QFont("Arial", 16))
        self.result_label_levante.setStyleSheet("color: white; background-color: rgba(255, 255, 255, 0.1); padding: 10px;")
        self.result_label_levante.setAlignment(Qt.AlignCenter)
        self.result_label_levante.setVisible(False)  # Oculta inicialmente

        # Layout de datas
        date_layout = QHBoxLayout()
        date_layout.addWidget(entrada_container_label)
        date_layout.addWidget(self.entrada_container)
        date_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        date_layout.addWidget(saida_container_label)
        date_layout.addWidget(self.saida_container)
        date_layout.setAlignment(Qt.AlignCenter)

        # Inicializa o layout de tipo e quantidade e o adiciona ao layout principal
        self.tipo_quantidade_container = QVBoxLayout()
        self.add_tipo_quantidade_layout()

        # Ajuste para os botões se estenderem
        gerar_simulacao.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        salvar_pdf.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        action_buttons_layout.addWidget(gerar_simulacao)
        action_buttons_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        action_buttons_layout.addWidget(salvar_pdf)
        action_buttons_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        action_buttons_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout principal de widgets com espaçamento entre elementos
        left_layout = QVBoxLayout()
        # left_layout.addWidget(select_recinto_label)
        left_layout.addWidget(select_recinto)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # left_layout.addWidget(valor_cif_label)
        left_layout.addWidget(valor_cif)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # left_layout.addWidget(select_tipo_mercadoria_label)
        left_layout.addWidget(select_tipo_mercadoria)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        left_layout.addLayout(date_layout)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # left_layout.addWidget(periodo_armazenagem_label)
        left_layout.addWidget(self.periodo_armazenagem)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        left_layout.addLayout(self.tipo_quantidade_container)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # left_layout.addWidget(custos_label)
        left_layout.addWidget(custos)
        left_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        left_layout.addLayout(action_buttons_layout)
        #left_layout.addItem(QSpacerItem(25, 25, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Layout centralizado horizontalmente
        center_layout = QHBoxLayout()
        center_layout.addLayout(left_layout)

        # Layout da direita (right_layout)
        right_layout = QVBoxLayout()
        right_layout.addWidget(simulacao_group)
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.result_label_levante)
        result_layout.setContentsMargins(0, 70, 0, 0)  # Ajuste o valor 50 para aumentar/reduzir o espaço
        right_layout.addLayout(result_layout)
        right_layout.addSpacerItem(QSpacerItem(0, 580, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Espaçador à esquerda

        # Adição dos layouts ao layout de conteúdo com espaçamento
        content_layout.addSpacerItem(QSpacerItem(485, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Espaçador à esquerda
        content_layout.addLayout(center_layout)  # Adiciona o layout centralizado
        content_layout.addSpacerItem(QSpacerItem(535, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Espaçador à direita
        content_layout.addLayout(right_layout)  # Adiciona o layout à direita
        content_layout.addSpacerItem(QSpacerItem(800, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Espaçador à direita

        # Adição dos layouts ao layout principal
        main_layout.addItem(QSpacerItem(0, 44, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(top_layout)
        main_layout.addItem(QSpacerItem(0, 109, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.entrada_container.dateChanged.connect(self.update_period)
        self.saida_container.dateChanged.connect(self.update_period)

        gerar_simulacao.clicked.connect(self.calculate_simulation)

    def calculate_simulation(self):
        recinto = self.select_recinto.currentText()
        tipo_mercadoria = self.select_tipo_mercadoria.currentText()
        periodo_armazenagem = self.create_combobox_armazenagem.currentText()

        # Verificar se as condições gerais são atendidas
        if recinto == "PORTONAVE" and tipo_mercadoria == "NORMAL" and periodo_armazenagem == "1º período":
            valor_total = 0  # Inicializar o valor total para serviços extras
            valor_total_levante = 0  # Inicializar o valor total para levantes

            # Iterar sobre todos os tipos e quantidades de contêineres adicionados
            for i in range(len(self.quantidade_container_list)):
                tipo_conteiner = self.tipo_container_list[i].currentText()
                quantidade_container = self.quantidade_container_list[i]

                # Apenas continuar se o tipo de contêiner for válido
                try:
                    quantidade = int(quantidade_container.text())
                except ValueError:
                    quantidade = 1  # Usar valor padrão de 1 se não for um número válido

                # Calcular os serviços extras multiplicando pela quantidade
                valor_total += sum(self.selected_options_values.values()) * quantidade

                # Cálculo específico para o tipo de contêiner no valor_total_levante
                if tipo_conteiner == "Normal":
                    valor_total_levante += 375.99 * quantidade
                elif tipo_conteiner == "Open Top":
                    valor_total_levante += 967.00 * quantidade
                elif tipo_conteiner == "Flat Rack":
                    valor_total_levante += 967.00 * quantidade
                elif tipo_conteiner == "Carga solta":
                    valor_total_levante += 0.00 * quantidade  # Atualização para Carga solta

            # Exibir o valor calculado para os serviços extras
            self.result_label.setText(f"Serviços extras: R$ {valor_total:.2f}")
            self.result_label.setVisible(True)

            # Exibir o valor calculado para o tipo de contêiner (levante)
            if not hasattr(self, 'result_label_levante'):
                self.result_label_levante = QLabel()  # Certifique-se de que result_label_levante é inicializado
            self.result_label_levante.setText(f"Levante: R$ {valor_total_levante:.2f}")
            self.result_label_levante.setVisible(True)
        else:
            # Ocultar os valores se as condições não forem atendidas
            self.result_label.setVisible(False)
            if hasattr(self, 'result_label_levante'):
                self.result_label_levante.setVisible(False)

    def resize_to_full_screen(self):
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.resize(size)
        self.showMaximized()

    def set_background_image(self):
        palette = QPalette()
        pixmap = QPixmap("C:\\Users\\rafael.souza.CAPITAL\\OneDrive - CAPITAL TRADE\\Área de Trabalho\\Documentos\\Python\\Calculadora\\bkg_CT_2024_calculadora.png")
        scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source is self:
            self.set_background_image()  # Update the background image on resize
        return super().eventFilter(source, event)
    
    def create_combobox_recinto(self, placeholder):
        combobox = QComboBox()
        combobox.addItem(placeholder) # Placeholder
        combobox.addItem("CLIF") # Opção 1
        combobox.addItem("ITAPOA") # Opção 2
        combobox.addItem("PORTONAVE") # Opção 3
        combobox.setMinimumWidth(420)
        combobox.setStyleSheet(self.get_combobox_style())
        
        # Desabilitar o placeholder para seleção
        combobox.model().item(0).setEnabled(False)
        self.select_recinto = combobox  # Armazenar o combobox para uso posterior
        
        return combobox
    
    def create_combobox_mercadoria(self, placeholder):
        combobox = QComboBox()
        combobox.addItem(placeholder)  # Placeholder
        combobox.addItem("NORMAL") # Opção 1
        combobox.addItem("IMO") # Opção 2
        combobox.addItem("OVERSIZE") # Opção 3
        combobox.addItem("REEFER") # Opção 4
        combobox.addItem("OVERSIZE IMO") # Opção 5
        combobox.setMinimumWidth(420)
        combobox.setStyleSheet(self.get_combobox_style())
        
        # Desabilitar o placeholder para seleção
        combobox.model().item(0).setEnabled(False)
        self.select_tipo_mercadoria = combobox  # Armazenar o combobox para uso posterior

        return combobox
    
    def create_combobox_conteiner(self, placeholder):
        combobox = QComboBox()
        combobox.addItem(placeholder)   # Placeholder
        combobox.addItem("Normal")      # Opção 1
        combobox.addItem("Open Top")    # Opção 2
        combobox.addItem("Flat Rack")   # Opção 3
        combobox.addItem("Carga Solta") # Opção 4
        combobox.setMinimumWidth(420)
        combobox.setStyleSheet(self.get_combobox_style())

        # Desabilitar o placeholder para seleção
        combobox.model().item(0).setEnabled(False)

        # Aqui você pode armazenar o combobox criado para ser usado posteriormente
        if not hasattr(self, 'combobox_list'):
            self.combobox_list = []
        
        # Armazenar o combobox na lista para acessar posteriormente
        self.combobox_list.append(combobox)
        
        return combobox

    def create_combobox_armazenagem(self, placeholder):
        combobox = QComboBox()
        combobox.addItem(placeholder)  # Placeholder
        combobox.addItem("1º período")  # Opção 1
        combobox.addItem("2º período")  # Opção 2
        combobox.addItem("3º período")  # Opção 3
        combobox.addItem("4º período")  # Opção 4
        combobox.setMinimumWidth(420)
        combobox.setStyleSheet(self.get_combobox_style())
        
        # Desabilitar o placeholder para seleção
        combobox.model().item(0).setEnabled(False)
        self.create_combobox_armazenagem = combobox  # Armazenar o combobox para uso posterior
        
        return combobox
    
    def update_period(self):
        entrada = self.entrada_container.date()
        saida = self.saida_container.date()
        
        difference = entrada.daysTo(saida)

        if difference >= 0:
            # Selecionar o período correspondente
            if difference <= 7:
                self.periodo_armazenagem.setCurrentIndex(1)  # 1º período
            elif 8 <= difference <= 14:
                self.periodo_armazenagem.setCurrentIndex(2)  # 2º período
            elif 15 <= difference <= 29:
                self.periodo_armazenagem.setCurrentIndex(3)  # 3º período
            else:
                self.periodo_armazenagem.setCurrentIndex(4)  # 4º período

            # Desabilitar a edição do combo box após a seleção
            self.periodo_armazenagem.setEnabled(False)

    def create_combobox(self, placeholder):
        button = QToolButton()
        button.setText(placeholder)  # Placeholder
        button.setPopupMode(QToolButton.InstantPopup)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        button.setStyleSheet(self.get_toolbutton_style())

        # Criação do menu personalizado
        menu = QMenu(button)

        # Widget para conter a lista de ações (checkboxes)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Dicionário de opções e valores
        options_values = {
            "Posicionamento para vistoria": 1071.00,
            "Posicionamento para pesagem": 1071.00,
            "Posicionamento para vistoria scanner": 2000.00,
            "Posicionamento para expurgo": 1187.00,
            "Vistoria scanner": 929.00,
            "Posicionamento desova/ova (Dry)": 4429.00,
            "Posicionamento desova/ova (Reefer)": 4915.00,
            "Posicionamento desova/ova de mudança": 12780.00,
            "Crossdocking (Dry)": 2521.00,
            "Crossdocking (Reefer)": 2885.00,
            "Movimento liberação DTA": 1719.00,
            "Remoneação de navio ou porto - exportação": 750.00,
            "Remoneação de navio ou porto - importação": 1049.00,
            "Retirada de amostras": 220.00,
            "Desmembramento de pallets": 17.00,
            "Etiquetagem": 8.00,
            "Disponibilização carreta contenção": 4164.00,
            "Diária carreta contenção": 3329.00,
            "Retirada e colocação de lacre": 126.00,
            "Pesagem de Contêiner (saída via gate)": 125.99,
            "Solicitação especial de agendamento de importação": 613.00,
            "Fornecimento de fotografias": 105.00,
            "Genset": 1288.00,
            "NO SHOW - Importação": 393.00,
            "Posicionamento inclusão de adesivos de carga perigosa": 1096.00
        }

        self.selected_options = set()

        # Adicionando checkboxes ao menu
        for option, value in options_values.items():
            checkbox = QCheckBox(f"{option}")
            checkbox.setChecked(False)
            # Conectar a função update_selected_options com a opção e o valor corretos
            checkbox.stateChanged.connect(lambda state, opt=option, val=value: self.update_selected_options(opt, val, state, button))
            scroll_layout.addWidget(checkbox)

        # Configurar a área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setFixedHeight(150)  # Ajuste conforme necessário
        scroll_area.setFixedWidth(1118)

        # Widget para o layout principal
        container_widget = QWidget()
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(scroll_area)

        # Adicionar o widget de rolagem ao menu
        container_action = QWidgetAction(menu)
        container_action.setDefaultWidget(container_widget)
        menu.addAction(container_action)

        # Define o menu personalizado para o botão
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setMenu(menu)

        return button

    def update_selected_options(self, option, value, checked, button):
        # Atualizar o conjunto de opções selecionadas e armazenar os valores
        if checked:
            self.selected_options.add(option)
            self.selected_options_values[option] = value  # Armazena o valor
        else:
            self.selected_options.discard(option)
            if option in self.selected_options_values:
                del self.selected_options_values[option]  # Remove o valor

        # Atualizar o texto do botão com as opções selecionadas
        if self.selected_options:
            button.setText("; ".join(sorted(self.selected_options)))
        else:
            button.setText("CUSTOS")  # Texto padrão

    def create_lineedit(self, placeholder):
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setText("") 
        
        def on_text_changed(text):
            if not text.startswith(""):
                line_edit.setText("")
            elif len(text) > 0:
                value = text[0:]
                if not value.isdigit():
                    line_edit.setText("" + ''.join(filter(str.isdigit, value)))
        line_edit.textChanged.connect(on_text_changed)
        line_edit.setStyleSheet(self.get_lineedit_style())
        self.quantidade_container = line_edit  # Armazenar o line edit para uso posterior
        return line_edit

    def create_lineedit_CIF(self, placeholder): 
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setText("VALOR CIF (R$)")  # Texto inicial com "R$ 0,00"
        
        # Limitar entrada apenas para números e permitir formatação com duas casas decimais
        def on_text_changed(text):
            if not text.startswith("R$ "):
                line_edit.setText("R$ 0,00")  # Garante que o prefixo "R$ " e valor inicial sejam sempre exibidos
            else:
                value = text[3:].replace(",", "").replace(".", "")  # Remove pontuações (vírgulas e pontos)

                if value.isdigit():
                    # Limitar o número de dígitos antes das casas decimais a 15
                    if len(value) > 16:
                        value = value[:16]

                    value = int(value)  # Converter a string para número
                    formatted_value = f"{value / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    line_edit.setText(f"R$ {formatted_value}")  # Formata o valor com duas casas decimais
                else:
                    # Remover caracteres inválidos e formatar corretamente
                    clean_value = ''.join(filter(str.isdigit, value))
                    if clean_value:
                        value = int(clean_value)
                        formatted_value = f"{value / 100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        line_edit.setText(f"R$ {formatted_value}")
                    else:
                        line_edit.setText("R$ 0,00")

        line_edit.textChanged.connect(on_text_changed)

        line_edit.setStyleSheet(self.get_lineedit_style())
        return line_edit

    def create_dateedit(self):
        dateedit = CustomDateEdit()
        dateedit.setDisplayFormat("dd/MM/yyyy")
        dateedit.setMinimumWidth(420)  # Define a largura mínima
        dateedit.setStyleSheet(self.get_dateedit_style())
        dateedit.setDate(QDate.currentDate())  # Define a data atual como padrão
        return dateedit

    def create_button(self, text, is_action_button=False):
        button = QPushButton(text)
        button.setMinimumWidth(220)
        if is_action_button:
            button.setStyleSheet(self.get_action_button_style())
        else:
            button.setStyleSheet(self.get_left_button_style())
        return button

    def create_plus_button(self):
        button = QPushButton("+")
        button.setFixedWidth(55)
        button.setStyleSheet(self.get_left_button_style())
        button.clicked.connect(self.add_tipo_quantidade_layout)
        return button

    def create_minus_button(self):
        button = QPushButton("-")
        button.setFixedWidth(55)
        button.setStyleSheet(self.get_left_button_style())
        button.clicked.connect(self.remove_tipo_quantidade_layout)
        return button

    def add_tipo_quantidade_layout(self):
        if self.tipo_quantidade_container.count() < 5:
            tipo_container = self.create_combobox_conteiner("TIPO DE CONTÊINER")
            quantidade_container = self.create_lineedit("QUANTIDADE DE CONTÊINER(ES)")
            plus_button = self.create_plus_button()
            minus_button = self.create_minus_button()

            # Armazenar os campos criados para garantir que não sejam deletados
            if not hasattr(self, 'tipo_container_list'):
                self.tipo_container_list = []
            if not hasattr(self, 'quantidade_container_list'):
                self.quantidade_container_list = []

            self.tipo_container_list.append(tipo_container)
            self.quantidade_container_list.append(quantidade_container)

            # Ajuste de altura dos campos
            tipo_container.setMinimumHeight(30)
            quantidade_container.setMinimumHeight(30)
            plus_button.setFixedHeight(30)
            minus_button.setFixedHeight(30)

            # Criar layout
            tipo_quantidade_layout = QHBoxLayout()
            tipo_quantidade_layout.addWidget(tipo_container, 6)
            tipo_quantidade_layout.addWidget(quantidade_container, 3)
            tipo_quantidade_layout.addWidget(plus_button, 1)
            tipo_quantidade_layout.addWidget(minus_button, 1)
            tipo_quantidade_layout.setSpacing(5)

            container_widget = QWidget()
            container_widget.setLayout(tipo_quantidade_layout)
            container_widget.setContentsMargins(0, 0, 0, 0)
            tipo_quantidade_layout.setContentsMargins(0, 0, 0, 0)

            self.tipo_quantidade_container.setSpacing(15)
            self.tipo_quantidade_container.addWidget(container_widget)

            # Conectar o botão de menos para remover o layout
            minus_button.clicked.connect(self.remove_tipo_quantidade_layout)

    def remove_tipo_quantidade_layout(self):
        # Garantir que haja mais de um layout antes de remover
        if self.tipo_quantidade_container.count() > 1:
            # Obter o último widget a ser removido
            item = self.tipo_quantidade_container.itemAt(self.tipo_quantidade_container.count() - 1)
            if item:
                widget = item.widget()
                if widget:
                    self.tipo_quantidade_container.removeWidget(widget)
                    widget.deleteLater()  # Evitar o RuntimeError

            # Remover os últimos elementos das listas de tipos e quantidades
            if self.tipo_container_list:
                self.tipo_container_list.pop()
            if self.quantidade_container_list:
                self.quantidade_container_list.pop()

            # Chamar a função para recalcular os valores
            self.calculate_simulation()

    def get_combobox_style(self):
        return """
            QComboBox {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border: none;
                border-radius: 10px;
                height: 60px;
                padding-left: 10px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: rgba(255, 255, 255, 0.25);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(arrow_down.png);
            }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 0.65);
                color: #003251;
                border: none;
                selection-background-color: rgba(255, 255, 255, 0.25);
            }
        """
    
    def get_toolbutton_style(self):
        return """
            QToolButton {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border: none;
                border-radius: 10px;
                height: 50px;
                padding-left: 10px;
                min-width: 0;
                max-width: 16777215;
            }
            QToolButton::menu-indicator {
                image: url(arrow_down.png);
                subcontrol-position: right;
                width: 10px;
                border-left-width: 1px;
                border-left-color: rgba(255, 255, 255, 0.25);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QWidget {
                background-color: rgba(255, 255, 255, 0.25); /* Fundo translúcido */
                border-radius: 8px;
                padding: 1px; /* Espaço ao redor dos checkboxes */
                border: 1px solid rgba(0, 0, 0, 0.1); /* Simulando a sombra com borda */
            }
            
            QCheckBox {
                color: #003251;  /* Cor do texto dos checkboxes */
                font-size: 14px;  /* Tamanho da fonte maior para melhorar a visibilidade */
                padding: 5px;
            }
            QCheckBox::indicator {
                background-color: rgba(255, 255, 255, 0.25);  /* Fundo com transparência */
                border: 2px solid rgba(255, 255, 255, 0.5);  /* Borda mais espessa e clara */
                border-radius: 5px;  /* Borda levemente arredondada */
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:checked {
                background-color: #003251;  /* Fundo azul escuro ao ser selecionado */
                border: 2px solid #005f8d;  /* Borda azul escura */
            }
            QCheckBox::indicator:hover {
                background-color: rgba(255, 255, 255, 0.4);  /* Fundo levemente mais claro ao passar o mouse */
            }
            
            /* Estilo da barra de rolagem vertical */
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.25);
                width: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px; /* Curvatura moderna */
            }

            /* Estilo da parte que pode ser arrastada */
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.4);
                min-height: 30px;
                border-radius: 6px; /* Curvatura moderna */
            }

            /* Setas da barra de rolagem, escondidas para um design mais limpo */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
                height: 0px;
            }

            /* Espaço acima e abaixo da barra de rolagem */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: rgba(0, 0, 0, 0.1);
            }

            /* Ao passar o mouse, muda a cor para indicar interatividade */
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.6);
            }
        """

    def get_lineedit_style(self):
        return """
            QLineEdit, QDateEdit {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border-radius: 10px;
                height: 60px;
                border: none;
                padding-left: 10px;
            }
        """

    def get_dateedit_style(self):
        return """
            QDateEdit {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border-radius: 10px;
                height: 60px;
                border: none;
                padding-left: 10px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: rgba(255, 255, 255, 0.25);
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
                background-color: rgba(255, 255, 255, 0.25); /* Background color for drop-down button */
            }
            QDateEdit QAbstractItemView {
                background-color: rgba(255, 255, 255, 0.25); /* Background color for drop-down items */
                color: white;
                border: none;
                selection-background-color: rgba(255, 255, 255, 0.35); /* Color when an item is selected */
            }
            QCalendarWidget {
                border: 1px solid rgba(255, 255, 255, 0.25);
                background-color: rgba(255, 255, 255, 0.25); /* Background color for calendar widget */
            }
            QCalendarWidget QAbstractItemView {
                background-color: rgba(255, 255, 255, 0.25); /* Background color for calendar items */
                color: white;
                selection-background-color: rgba(255, 255, 255, 0.35); /* Color when an item is selected */
            }
        """

    def get_action_button_style(self):
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border: none;
                border-radius: 10px;
                height: 60px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.35);
            }
        """

    def get_left_button_style(self):
        return """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.25);
                color: white;
                border: none;
                border-radius: 5px;
                height: 60px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.35);
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StorageCalculator()
    window.resize_to_full_screen()
    sys.exit(app.exec())