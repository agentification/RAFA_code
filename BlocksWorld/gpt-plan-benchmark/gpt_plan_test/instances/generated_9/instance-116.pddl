

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(ontable c)
(on d f)
(on e b)
(on f i)
(on g c)
(ontable h)
(on i a)
(clear d)
(clear e)
(clear h)
)
(:goal
(and
(on b d)
(on c a)
(on e f)
(on g c)
(on h e)
(on i h))
)
)


