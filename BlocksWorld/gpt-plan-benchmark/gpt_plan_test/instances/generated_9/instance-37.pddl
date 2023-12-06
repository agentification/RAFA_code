

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(on b a)
(ontable c)
(ontable d)
(on e f)
(on f i)
(on g c)
(ontable h)
(on i h)
(clear b)
(clear d)
(clear e)
)
(:goal
(and
(on a i)
(on e d)
(on f b)
(on g c)
(on h f)
(on i g))
)
)


