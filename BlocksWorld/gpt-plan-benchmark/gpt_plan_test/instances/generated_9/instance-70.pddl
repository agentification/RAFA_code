

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b f)
(on c g)
(ontable d)
(on e i)
(on f h)
(on g b)
(on h e)
(ontable i)
(clear a)
(clear d)
)
(:goal
(and
(on a b)
(on b i)
(on c f)
(on d c)
(on f g)
(on h a)
(on i e))
)
)


