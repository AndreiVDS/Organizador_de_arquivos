import os
import shutil
import time
import logging
from tkinter.filedialog import askdirectory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)

# Lista global para armazenar os processos em segundo plano
processos_em_execucao = []

# Funções utilitárias para verificar o tipo de arquivo
def extension_type(file_path):
    try:
        _, ext = os.path.splitext(file_path)
        return ext.lower()  # Retorna a extensão em minúsculas
    except ValueError:
        logging.error(f'Arquivo sem extensão detectado: {file_path}')
        return None

def is_fiscal_file(file_path):
    return extension_type(file_path) in ('.txt', '.xml', '.log')

def is_compress_file(file_path):
    return extension_type(file_path) in ('.zip', '.rar', '.tar', '.gz', '.7z')

def is_pdf_file(file_path):
    return extension_type(file_path) == '.pdf'

def is_audio_file(file_path):
    return extension_type(file_path) in ('.mp3', '.wav', '.aac', '.flac', '.ogg')

def is_image_file(file_path):
    return extension_type(file_path) in ('.png', '.jpg', '.bmp', '.gif', '.raw', '.tiff', '.svg', '.jpeg')

def is_video_file(file_path):
    return extension_type(file_path) in ('.mp4', '.avi', '.flv', '.mkv', '.wmv', '.mov')

def is_doc_file(file_path):
    return extension_type(file_path) in ('.doc', '.docx')

def is_spreadsheet_file(file_path):
    return extension_type(file_path) in ('.xls', '.xlsx', '.ods', '.odt', '.csv', '.odp', '.rtf')

def is_presentation_file(file_path):
    return extension_type(file_path) in ('.ppt', '.pptx')

def is_code_file(file_path):
    return extension_type(file_path) in ('.py', '.cs', '.js', '.php', '.html', '.sql', '.css', '.db', '.mdb', '.sqlite')

def is_windows_file(file_path):
    return extension_type(file_path) in ('.exe', '.msi', '.ink', '.dll', '.sys', '.ini', '.bat')

def make_folder(base_path, foldername):
    folder_path = os.path.join(base_path, foldername)
    
    if os.path.exists(folder_path):
        logging.info(f'Folder already exists: {folder_path}')
    else:
        os.mkdir(folder_path)
        logging.info(f'Created folder: {folder_path}')
    
    return folder_path

def move_to_new_corresponding_folder(file_path, path_to_new_folder):
    for _ in range(5):  # Tenta 5 vezes
        try:
            shutil.move(file_path, path_to_new_folder)
            logging.info(f'Moving file {file_path} to {path_to_new_folder}')
            return  # Sai da função se for bem-sucedido
        except FileExistsError:
            logging.error(f'File already existed in target folder: {file_path}')
            return
        except PermissionError:
            logging.warning(f'The file is being used by another process: {file_path}. Retrying...')
            time.sleep(1)  # Espera 1 segundo antes de tentar novamente
        except Exception as e:
            logging.error(f'Unexpected error moving file {file_path}: {e}')
            return
    logging.error(f'Failed to move file after multiple attempts: {file_path}')

def log_extension_in_others_folder(others_folder, extension):
    with open(os.path.join(others_folder, 'extensoes.txt'), 'a') as ext_file:
        ext_file.write(f'{extension}\n')

def organize_existing_files(base_path, file_type):
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isfile(item_path):
            file_ext = extension_type(item_path)
            if file_type in ['todos', '1'] and is_code_file(item_path):
                path_to_folder = make_folder(base_path, 'Arquivos de Códigos')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '2'] and is_fiscal_file(item_path):
                path_to_folder = make_folder(base_path, 'texto e xml')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '3'] and is_compress_file(item_path):
                path_to_folder = make_folder(base_path, 'Arquivos Compactados')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '4'] and is_pdf_file(item_path):
                path_to_folder = make_folder(base_path, 'pdf')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '5'] and is_audio_file(item_path):
                path_to_folder = make_folder(base_path, 'audio')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '6'] and is_image_file(item_path):
                path_to_folder = make_folder(base_path, 'imagens')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '7'] and is_video_file(item_path):
                path_to_folder = make_folder(base_path, 'videos')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '8'] and is_doc_file(item_path):
                path_to_folder = make_folder(base_path, 'Documentos do word')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '9'] and is_spreadsheet_file(item_path):
                path_to_folder = make_folder(base_path, 'Planilhas')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '10'] and is_presentation_file(item_path):
                path_to_folder = make_folder(base_path, 'Arquivos de apresentação')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type in ['todos', '11'] and is_windows_file(item_path):
                path_to_folder = make_folder(base_path, 'Arquivos do Windows')
                move_to_new_corresponding_folder(item_path, path_to_folder)
            elif file_type == 'todos':
                path_to_folder = make_folder(base_path, 'outros')
                move_to_new_corresponding_folder(item_path, path_to_folder)
                log_extension_in_others_folder(path_to_folder, file_ext)

# Classe para lidar com eventos de sistema de arquivos
class Handler(FileSystemEventHandler):
    def __init__(self, base_path, file_types):
        self.base_path = base_path
        self.file_types = file_types
    
    def on_created(self, event):
        logging.info(f'Arquivo criado: {event.src_path}')
    
    def on_modified(self, event):
        if os.path.isdir(event.src_path):
            return
        file_path = event.src_path
        file_ext = extension_type(file_path)
        try:
            for file_type in self.file_types:
                if file_type in ['todos', '1'] and is_code_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Arquivos de Códigos')
                elif file_type in ['todos', '2'] and is_fiscal_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'texto e xml')
                elif file_type in ['todos', '3'] and is_compress_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Arquivos Compactados')
                elif file_type in ['todos', '4'] and is_pdf_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'pdf')
                elif file_type in ['todos', '5'] and is_audio_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'audio')
                elif file_type in ['todos', '6'] and is_image_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'imagens')
                elif file_type in ['todos', '7'] and is_video_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'videos')
                elif file_type in ['todos', '8'] and is_doc_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Documentos do word')
                elif file_type in ['todos', '9'] and is_spreadsheet_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Planilhas')
                elif file_type in ['todos', '10'] and is_presentation_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Arquivos de apresentação')
                elif file_type in ['todos', '11'] and is_windows_file(file_path):
                    path_to_folder = make_folder(self.base_path, 'Arquivos do Windows')
                elif file_type == 'todos':
                    path_to_folder = make_folder(self.base_path, 'outros')
                    log_extension_in_others_folder(path_to_folder, file_ext)
                else:
                    continue  # Não organiza se o tipo de arquivo não foi especificado
                move_to_new_corresponding_folder(file_path, path_to_folder)
                logging.info(f'Arquivo {file_path} movido para {path_to_folder}')
                break
        except Exception as e:
            logging.error(f"Erro ao mover o arquivo {file_path}: {e}")

    def on_deleted(self, event):
        logging.info(f'Arquivo deletado: {event.src_path}')

    def on_moved(self, event):
        logging.info(f'Arquivo movido: {event.src_path} para {event.dest_path}')

# Função para listar os processos em execução
def listar_processos():
    if not processos_em_execucao:
        print("Nenhum processo em execução.")
    else:
        for i, processo in enumerate(processos_em_execucao, 1):
            print(f"{i}. Observando pasta: {processo['path']}")

# Função para matar um processo específico
def matar_processo(index):
    try:
        processo = processos_em_execucao.pop(index - 1)
        processo['observer'].stop()
        processo['observer'].join()
        logging.info(f"Monitoramento da pasta {processo['path']} encerrado.")
    except IndexError:
        print("Índice inválido. Por favor, tente novamente.")
        
def matar_processos(indices):
    indices.sort(reverse=True)  # Ordena os índices em ordem decrescente para evitar problemas ao remover
    for index in indices:
        try:
            processo = processos_em_execucao.pop(index - 1)
            processo['observer'].stop()
            processo['observer'].join()
            logging.info(f"Monitoramento da pasta {processo['path']} encerrado.")
        except IndexError:
            print(f"Índice inválido: {index}. Por favor, tente novamente.")

# Função principal para iniciar o monitoramento
def start_monitoring():
    while True:
        caminho = askdirectory(title="Selecione uma pasta para organizar seus arquivos")

        if not caminho:
            logging.info('Nenhuma pasta selecionada. Encerrando...')
            return

        while True:
            file_types = input("Quais tipos de arquivo você deseja organizar?\n 1-codigo\n 2-fiscal\n 3-compactado\n 4-pdf\n 5-audio\n 6-imagem\n 7-video\n 8-documento\n 9-planilha\n 10-apresentação\n 11-arquivos do windows\n todos\n (Ex.: 1 ou 1,2,3): ").strip().lower().split(',')
            file_types = [ftype.strip() for ftype in file_types if ftype.strip()]

            for file_type in file_types:
                organize_existing_files(caminho, file_type)

            file_change_handler = Handler(caminho, file_types)
            observer = Observer()
            observer.schedule(file_change_handler, caminho, recursive=False)
            observer.start()

            processos_em_execucao.append({"path": caminho, "observer": observer})

        
            while True:
                    continuar = input("Concluído com sucesso!! Deseja continuar organizando esta pasta? (sim/não/nova/ver/listar): ").strip().lower()
                    if continuar in ["sim", "s"]:
                        logging.info("Continuando a organizar a pasta.")
                        break
                    elif continuar in ["não", "nao", "n"]:
                        observer.stop()
                        observer.join()
                        logging.info("Monitoramento encerrado pelo usuário.")
                        return
                    elif continuar == "nova":
                        observer.stop()
                        observer.join()
                        caminho = askdirectory(title="Selecione uma pasta para organizar seus arquivos")
                        if not caminho:
                            logging.info('Nenhuma pasta selecionada. Encerrando...')
                            return
                        break
                    elif continuar == "ver":
                        listar_processos()
                    elif continuar == "listar":
                        listar_processos()
                    elif continuar.startswith("matar"):
                        try:
                            indices = list(map(int, continuar.split()[1:]))  # Supondo que o usuário digite "matar 1 2 3"
                            matar_processos(indices)
                        except ValueError:
                            print("Comando inválido. Use 'matar <número> <número>...'.")
                        except KeyboardInterrupt:
                            observer.stop()
                            observer.join()

if __name__ == "__main__":
    start_monitoring()
