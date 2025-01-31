class PingView:
    def display_results(self, results):
        print("ping Results:\n")
        for result in results:
            print(result)
            
    def display_error(self, error_message):
        print(f"An error occured: {error_message}")
        
    def display_message(self, message):
        print(message)