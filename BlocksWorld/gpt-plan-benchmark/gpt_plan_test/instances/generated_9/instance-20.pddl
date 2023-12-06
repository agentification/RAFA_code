

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(ontable c)
(on d e)
(on e f)
(on f b)
(on g d)
(ontable h)
(on i a)
(clear c)
(clear h)
(clear i)
)
(:goal
(and
(on a g)
(on b a)
(on c i)
(on e b)
(on f d)
(on h e))
)
)


