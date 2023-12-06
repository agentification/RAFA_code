

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(on b c)
(ontable c)
(on d i)
(on e f)
(ontable f)
(on g d)
(on h e)
(on i h)
(clear a)
(clear b)
)
(:goal
(and
(on c g)
(on d h)
(on e d)
(on f e)
(on g a))
)
)


