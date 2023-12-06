

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b d)
(ontable c)
(ontable d)
(on e f)
(on f b)
(ontable g)
(on h e)
(ontable i)
(clear a)
(clear c)
(clear g)
(clear h)
(clear i)
)
(:goal
(and
(on b a)
(on e h)
(on f d)
(on g e)
(on h b)
(on i c))
)
)


