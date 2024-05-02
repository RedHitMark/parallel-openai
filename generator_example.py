import jsonl_utils


if __name__ == '__main__':
    for i in range(1):
        model_data = {
            "id": i,
            "model": f'gpt-3.5-turbo-0125',
            "messages": [
                {
                    "role": "system",
                    "content": 'Sei un esperto linguista il cui compito è quello di riscrivere dei documenti istituzionali per rendili semplici e comprensibili. Ti verrà fornito un testo proveniente da un documento e il tuo compito sarà quello di riscrivere il testo applicando diverse regole di semplificazione senza però modificare il significato originale del testo. Ad esempio potresti rendere le frasi più brevi, eliminare le perifrasi, esplicitare sempre il soggetto, utilizzare parole più semplici oppure trasformare i verbi in forma attiva.'
                },
                {
                    "role": "user",
                    "content": 'L\'operatore di Polizia Locale, quindi, rappresenta un importante punto di riferimento per la collettività. Nell\'ambito delle sue funzioni, esso svolge i propri compiti in maniera autorevole, dando prova di preparazione professionale e sensibilità nel contatto relazionale. La sua attività, inoltre, è caratterizzata dal costante sforzo teso alla migliore interpretazione delle situazioni e delle problematiche incontrate, applicando un approccio educativo e orientato alla più adeguata risposta ai bisogni della cittadinanza.'
                }
            ],
        }
        jsonl_utils.append_to_jsonl('source.jsonl', model_data)
