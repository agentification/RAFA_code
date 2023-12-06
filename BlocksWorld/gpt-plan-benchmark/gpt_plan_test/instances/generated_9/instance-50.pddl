

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(on c a)
(on d b)
(on e i)
(ontable f)
(on g f)
(ontable h)
(on i h)
(clear c)
(clear d)
(clear e)
)
(:goal
(and
(on a f)
(on b h)
(on c d)
(on g e)
(on h a)
(on i b))
)
)


