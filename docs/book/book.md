# Jacek Siciarek -Automaty komórkowe

Publikacja ta powstała z potrzeby przypomnienie wszystkim zainteresowanym informatyką
pewnej dziedziny, która była w informatyce obecna jeszcze przed wynalezieniem języków programowania,
teraz nieco zapomniana, poza pewnymi obszarami nauki, może jednak dostarczyć wrażeń programistom, którzy lubią zobqczyć efekt swojej pracy.

Automaty komórkowe, których konstrukcja jest piękna w swej prostocie potrafi jednak wygenerować efekty
które potrafią robić wrażenie na wrażliwym odbiorcy, zbliżone do tych wywoływanych przez dzieła artystów plastyków.

## Czym automat komórkowy jest, a czym nie jest

Zacznę od tego, że z całą pewnością {\em automat komórkowy} nie ma nic wspólnego z telefonią komórkową. To jest bardzo
ważne stwierdzenie bo nie będzie wprowadzać w błąd czytelnika.0

Czym zatem jest {\em automat komórkowy}? Na ten temat można znaleźć wiele definicji, to co opiszę poniżej stanowi
moją własną wypadkową tych definicji, sformułowaną w sposób zrozumiały zarówno dla początkującego czytelnika
jak i dla eksperta w temacie. Stanowi moją własną odpowiedź na pytanie, które zadaję komuś kto na danej rzeczy się zna
a ja nie i chcę przynajmniej zarys tematu poznać jak najszybciej, pytanie to brzmi:

Wytłumacz mi w 3 do 5 żołnierskich zdaniach czym jest automat komórkowy.

Oto odpowiedź, mam nadzieję że 5 zdań wystarczy.0

Automat komórkowy jest iteracyjna funkcją matematyczną.

Każdy krok tej funkcji na wejściu przyjmuje obecną `przestrzeń automatu komórkowego`
* prztwarzana jest komórka po komórkce i nowa wartość wyliczana jest na podstawie:
  - obecnego stanu komórki
  - innych wartości (np. wartości które posiadają sąsiednie komórki, lub w przypadku automatów niedetrministycznych wartości określane przez zmienną losową)
* po przeliczeniu ostatniej komórki nowa przestrzeń zajmuje miejsce dotyczasowej.
* przechodzimy do następnego kroku

* Części składowe Automatu komórkowego to:
  - przestrzeń automatu komórkowego (zazwyczaj modelowana jako macierz elementów zwanych komórkami)
  - zbiór stanów, który może przyjąć dana komórka
  - zbiór reguł, które na podstawie obecnego stanu komórki oraz innych warunków (np. stanów sąsiadujących komórek) zmienia stan wybranej komórki
  - początkowy stan automatu (krok 0) (jakie wartości przyjmują komórki automatu przed pierwszą iteracją)

Jeżeli mówimy `skończony` oznacza to, że może być dowolnie wielki ale niezmienny podczas każdej z iteracji.

## Przestrzeń automatu komórkowego

Jako przestrzeń automatu komórkowego zazwyczaj uważamy n-wymiarową siatkę. Najpopularniejsze to:

* siatka kwadratowa --- przstawiana jako powierzchnia wypełniona kwadratami
* siatka trójkątna --- przedstawiana jako powierzchnia wypełniona trójkątami rownobocznymi
* siatka heksagonalna --- powierzchnia wypełniona sześciokątami foremnymi

Po co używamy różnych typów? Odpowiedź jest prosta, chodzi o ilość komórek sąsiedztwa, bardzo przydatna w modelowaniu

* siatka kwadratowa - komórka ma 4 bezpośrednich sąsiadów (stykających się ścianami)
* siatka trójkątna - komórka ma 3 bezpośrednich sąsiadów (stykających się ścianami)
* siatka heksagonalna - komórka ma 6 bezpośrednich sąsiadów (stykających się ścianami)

