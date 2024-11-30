import grpc
import financial_service_pb2 as pb2
import financial_service_pb2_grpc as pb2_grpc
import uuid


def mostra_menu(client_id):
    menu = [
        "1) Registra utente",
        "2) Aggiorna utente",
        "3) Cancella utente",
        "4) Leggi ultimo valore",
        "5) Calcola valore medio",
        "0) Termina"
    ]
    print(f"\nClient ID: {client_id}")
    print("=" * 25)
    print("           MENU")
    print("=" * 25)
    for voce in menu:
        print(f"{voce.center(25)}")
    print("=" * 25)




def run():
    # Connessione al server gRPC
    target = 'localhost:50051'

    # Generazione casuale id utente e inizializzazione request_id = 0
    client_id = str(uuid.uuid4())
    request_id = 0 

    with grpc.insecure_channel(target) as channel:    
        stub = pb2_grpc.FinancialServiceStub(channel)

        
        while True:
            mostra_menu(client_id)

            # Leggi l'opzione da tastiera
            scelta = int(input("Inserisci il numero dell'opzione (0-5): "))   

            my_metadata = [
                ('client_id', client_id),
                ('request_id', str(request_id))
            ]     

              
            # Esegui l'azione in base alla scelta
            if scelta == 1:
                print("\n=== Registra Utente ===")
                email = input("\nInserisci email: ")
                ticker = input("\nInserisci ticker: ")
                register_request = pb2.UserRequest(email = email, ticker = ticker)
                register_response = stub.RegisterUser(register_request, metadata = my_metadata)
                print(f"Messaggio di risposta: {register_response.message} (Esito: {register_response.success})")
                request_id+=1

            elif scelta == 2:
                print("\n=== Aggiorna Utente ===")
                email = input("\nInserisci email: ")
                ticker = input("\nInserisci ticker: ")
                update_request = pb2.UserRequest(email=email, ticker=ticker)
                update_response = stub.UpdateUser(update_request, metadata = my_metadata)
                print(f"Messaggio di risposta: {update_response.message} (Esito: {update_response.success})")
                request_id+=1

            elif scelta == 3:
                print("\n=== Cancella Utente ===")
                email = input("\nInserisci email: ")
                delete_request = pb2.UserRequest(email=email)
                delete_response = stub.DeleteUser(delete_request, metadata = my_metadata)
                print(f"Messaggio di risposta: {delete_response.message} (Esito: {delete_response.success})")
                request_id+=1

            elif scelta ==4:
                print("\n=== Leggi ultimo valore ===")
                email = input("\nInserisci email: ")
                latest_value_request = pb2.UserRequest(email=email, ticker = 'AAPL')
                latest_value_response = stub.GetLatestValue(latest_value_request, metadata = my_metadata)
                if not latest_value_response.success:
                    print(f"Messaggio di risposta: {latest_value_response.message} (Esito: {latest_value_response.success})")
                else:
                    print(f"Ultimo valore: {latest_value_response.value}, Data: {latest_value_response.date} (Esito: {latest_value_response.success})")
                request_id+=1

            elif scelta ==5:
                print("\n=== Calcola valore medio ===")
                email = input("\nInserisci email: ")
                count = input("\nInserisci il numero di valori su cui calcolare il valore medio: ")
                
                try:
                    average_request = pb2.StockHistoryRequest(email= email, count = int(count))
                    average_response = stub.GetAverageValue(average_request, metadata = my_metadata)
                    if not average_response.success:
                        print(f"Messaggio di risposta: {average_response.message} (Esito: {average_response.success})")
                    else:
                        print(f"Valore medio: {average_response.value}, (Esito: {average_response.success})")
                except ValueError:
                    print("Errore: devi inserire un numero intero valido.")
                request_id+=1
                
            elif scelta == 0:
                print("\nClient terminato.")
                break
                               
            else: 
                print("\nOpzione non valida! Inserisci un numero tra 0 e 5.")



if __name__ == "__main__":
    run()


