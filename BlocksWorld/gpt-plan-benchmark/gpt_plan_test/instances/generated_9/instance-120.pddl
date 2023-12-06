

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(ontable b)
(on c a)
(on d i)
(on e d)
(on f h)
(on g c)
(on h g)
(on i b)
(clear f)
)
(:goal
(and
(on a e)
(on b f)
(on c g)
(on e c)
(on f i)
(on h a))
)
)


