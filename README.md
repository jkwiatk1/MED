# Reguły asocjacyjne
Dokumentacja projektowa:  https://github.com/jkwiatk1/MED/blob/main/docs/Dokumentacja.pdf

## Temat i cel projektu
Implementacja algorytmu Apriori do odkrywanie reguł asocjacyjnych pozwalająca na zastosowanie hierarchii elementów m.in. 3 poziomowej.
Należy dopuścić reguły a → Ah, gdzie a – jest element w transakcji, Ah - elementem z hierarchii, do którego jest przypisany m.in. element a, jeśli są transakcje
t: t ⊃ (a, b), a ∈ E(Ah) b ∈ E(Ah), gdzie E(y) - zbiór elementów przypisanych
do elementu y hierarchii.

Celem jest zbadanie własności algorytmu : czas wykonania, uzyskiwane wyniki dla różnych wartości parametrów algorytmu oraz różnej wielkości zbioru wejściowego.

## Zbiór danych 
Zbiór danych Fruithut pochodzi ze strony:
https://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php

* hierarchiczny, 4 poziomy zagnieżdżeń i 43 kategorie
* jest to zbiór danych zawierający transakcje klientów z amerykańskiego sklepu detalicznego, specjalizującego się w sprzedaży owoców. Zbiór danych zawiera 181 970 transakcji i 1 265 różnych przedmiotów. Największa
transakcja zawiera 36 przedmiotów, podczas gdy średnio klient kupuje 3,58 przedmiotów na transakcję.
* transakcje: https://www.philippe-fournier-viger.com/spmf/datasets/fruithut_original.txt
* taksonomia: https://www.philippe-fournier-viger.com/spmf/datasets/Fruithut_taxonomy_data.txt

## Założenia i implementacja 
Dokładne założenia oraz kwestie implementacyjne zostały opisane w dokumentacji projektowej. 

## Przykładowe uzyskane wyniki
Dokładna analiza uzyskanych wyników została opisana w dokumentacji. Tutaj umieszczono tylko przykładowe.