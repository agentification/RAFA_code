

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c e)
(on d i)
(on e b)
(on f g)
(on g h)
(on h d)
(ontable i)
(clear a)
(clear c)
)
(:goal
(and
(on c f)
(on d e)
(on e b)
(on f a)
(on h i))
)
)


