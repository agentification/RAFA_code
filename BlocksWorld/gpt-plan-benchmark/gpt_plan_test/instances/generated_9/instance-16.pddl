

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b g)
(on c i)
(on d c)
(on e f)
(ontable f)
(on g h)
(on h e)
(ontable i)
(clear a)
(clear d)
)
(:goal
(and
(on e c)
(on f d)
(on g f))
)
)


