

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(ontable b)
(on c d)
(on d b)
(on e f)
(on f h)
(on g e)
(ontable h)
(ontable i)
(clear a)
(clear c)
(clear i)
)
(:goal
(and
(on a h)
(on c f)
(on d e)
(on e i)
(on f g)
(on g a)
(on i c))
)
)


