# Problem Jedzących Filozofów

## Opis Zadania

Problem jedzących filozofów to klasyczny problem synchronizacji współbieżnych procesów, przedstawiony przez Edsgera Dijkstrę. Zadanie polega na zapewnieniu, że filozofowie (wątki) **mogą jeść i myśleć**, ale nigdy **nie dochodzi do zakleszczenia (deadlock)** ani **jednoczesnego jedzenia przez sąsiadów**.

W naszej implementacji użyto **muteksów (`std::mutex`) oraz zmiennych warunkowych (`std::condition_variable`)**, aby kontrolować dostęp do zasobów (widełek) i zapewnić sprawiedliwe przydzielanie czasu jedzenia.

---

## Sposób Działania

1. **Każdy filozof zaczyna od myślenia.**  
2. **Filozof, który chce jeść, sprawdza, czy jego sąsiedzi nie jedzą.**  
   - Jeśli tak, musi poczekać.  
   - Jeśli nie, podnosi oba widelce i zaczyna jeść.  
3. **Po zakończeniu jedzenia filozof odkłada widelce i ponownie zaczyna myśleć.**  
4. **Sąsiedzi są powiadamiani o dostępności widelców.**  

W programie zastosowano **trzy stany dla każdego filozofa**:
- `THINKING` – filozof myśli.
- `HUNGRY` – filozof chce jeść, ale czeka na dostępność widelców.
- `EATING` – filozof je.

---

## Uruchamianie Programu

Aby uruchomić program, skompiluj kod i uruchom plik wykonywalny, podając liczbę filozofów jako argument:

```sh
./dining_philosophers 5
```

## Dodatkowe informacje o implementacji rozwiązania
Główne mechanizmy użyte w implementacji:
- Muteks (std::mutex) – zapewnia synchronizację dostępu do widełek.
- Zmienna warunkowa (std::condition_variable) – pozwala filozofom czekać, aż widelce będą dostępne.
- Stan filozofów (THINKING, HUNGRY, EATING) – kontroluje dostęp do zasobów.
- Funkcja can_eat(int id) – sprawdza, czy filozof może rozpocząć jedzenie.
- Zapewniona sprawiedliwość – filozofowie nie głodują i nie blokują się wzajemnie.
