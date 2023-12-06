

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a i)
(ontable b)
(ontable c)
(on d c)
(on e h)
(on f d)
(ontable g)
(ontable h)
(on i g)
(clear a)
(clear b)
(clear e)
(clear f)
)
(:goal
(and
(on a c)
(on c h)
(on f b)
(on h d)
(on i e))
)
)


