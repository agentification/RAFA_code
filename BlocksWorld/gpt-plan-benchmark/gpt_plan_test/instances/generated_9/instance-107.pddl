

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(ontable b)
(ontable c)
(on d b)
(on e d)
(on f e)
(ontable g)
(on h f)
(ontable i)
(clear a)
(clear c)
(clear g)
(clear h)
(clear i)
)
(:goal
(and
(on a i)
(on b e)
(on c h)
(on d f)
(on e c)
(on h a)
(on i g))
)
)


