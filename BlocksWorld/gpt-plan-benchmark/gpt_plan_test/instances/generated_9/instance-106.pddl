

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(ontable b)
(on c d)
(on d g)
(on e f)
(ontable f)
(ontable g)
(on h c)
(ontable i)
(clear a)
(clear e)
(clear h)
(clear i)
)
(:goal
(and
(on c h)
(on d c)
(on f g)
(on g i)
(on h f)
(on i e))
)
)


