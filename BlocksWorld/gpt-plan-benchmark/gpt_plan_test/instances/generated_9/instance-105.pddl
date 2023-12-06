

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a g)
(on b f)
(ontable c)
(ontable d)
(on e b)
(on f h)
(on g e)
(ontable h)
(ontable i)
(clear a)
(clear c)
(clear d)
(clear i)
)
(:goal
(and
(on a e)
(on b f)
(on d c)
(on e i)
(on h a)
(on i d))
)
)


