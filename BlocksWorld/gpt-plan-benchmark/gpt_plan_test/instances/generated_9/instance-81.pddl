

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(ontable b)
(on c g)
(on d e)
(on e b)
(ontable f)
(on g d)
(on h f)
(ontable i)
(clear a)
(clear h)
(clear i)
)
(:goal
(and
(on b h)
(on c g)
(on d e)
(on e i)
(on f b)
(on g f)
(on i a))
)
)


