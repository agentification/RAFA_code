

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b a)
(on c d)
(on d h)
(on e i)
(ontable f)
(ontable g)
(on h g)
(on i c)
(clear b)
(clear f)
)
(:goal
(and
(on a g)
(on b i)
(on d a)
(on f e)
(on g f)
(on h d)
(on i c))
)
)


