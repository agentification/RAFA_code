

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(ontable b)
(on c g)
(on d c)
(on e d)
(on f a)
(ontable g)
(on h e)
(on i f)
(clear h)
(clear i)
)
(:goal
(and
(on a g)
(on d h)
(on e c)
(on g f)
(on i b))
)
)


